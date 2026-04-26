# Budgets App

A modular Python CLI application for tracking personal budgets and categorizing bank transactions from CSV exports.

## What it does

Read a CSV export of your bank transactions, automatically categorize each transaction by keyword (Groceries, Eating Out, Utilities, etc.), and compare actual expenditures against budgeted amounts you've set per category. Income and expense breakdowns are displayed as formatted tables; transactions that don't match any keyword are flagged as "Uncategorized" so you can recategorize them manually through the menu.

The full feature set:

- View current budgets with expenditures and remaining amounts
- Set, update, or delete budget amounts per category (twenty default categories included)
- Load a transaction CSV and automatically categorize each entry by description
- View transactions sorted by category, transaction number, or date
- Manually recategorize individual transactions
- Persist budget and transaction state across sessions in internally-managed CSV files

## A note on the data

The `csv/` directory contains **sanitized sample transactions** designed to exercise the categorizer's edge cases. Real personal financial data is not included, for obvious reasons. The samples use realistic bank-export formatting and cover a mix of income, expenses, and categorization edge cases (including the "animal hospital → Pet Care" / "grocery outlet → Groceries" / "amazon prime video → Entertainment" cases that the search-order tests verify).

## Setup and running

Requires Python 3.10+.

```
git clone https://github.com/SKnight-7/budgets-app-modular
cd budgets-app-modular
pip install -r requirements.txt
python budgets.py
```

On first launch, the app initializes the default budget categories and an empty transaction set. To work with your own data, save a bank CSV export into the `csv/` directory and load it through the menu (option 3 → enter the filename).

The app currently expects Wells Fargo's CSV export format: no headers, with columns `date, amount, asterisk, blank-or-check-number, description`. Other banks' formats can be supported by modifying `TransactionsManager.load_user_transactions` in `budgets.py`.

## Architecture

```
.
├── budgets.py             # Main entry point; manager and controller classes
├── budget_category.py     # BudgetCategory data class with validation
├── transaction.py         # Transaction data class with validation
├── default_categories.py  # 20 default budget categories with associated keywords
├── categorizer.py         # Pure function for matching descriptions to categories
├── menus.py               # Menu rendering helpers
├── ui.py                  # Display and input helpers, isolated from business logic
├── whimsy.py              # Launch flourish: figlet title + randomized cowsay greeting
├── csv/                   # Sample CSVs and runtime state files
├── tests/                 # Pytest test suite for the categorizer
└── conftest.py            # Pytest configuration
```

The application uses a layered design:

- **Data classes** (`Transaction`, `BudgetCategory`) hold values with validation enforced at the property setters, so invalid inputs are caught at the boundary rather than producing bad state downstream.
- **Manager classes** (`BudgetManager`, `TransactionsManager`) handle persistence and the domain logic for their respective concerns.
- **Controller** (`FinancialController`) orchestrates between the managers; the `main()` loop only ever interacts with this class, never reaching into the managers directly.
- **Presentation** (`ui.py`, `menus.py`, `whimsy.py`) is isolated from business logic, so the same data could be presented through a different interface (a web app, a GUI, anything) without changing the core code.

## The categorizer's search_order mechanism

The most interesting design decision in the codebase is how `categorize_item` resolves ambiguous matches. Each `BudgetCategory` has a `search_order` integer; the categorizer iterates categories in ascending order and returns the first one whose keywords appear in the transaction description.

This matters because real bank descriptions frequently contain keywords from multiple categories. Without ordering, the result would be unpredictable. With it, the design intent is explicit:

| Description | Matches | Wins because... |
|---|---|---|
| `ANIMAL HOSPITAL EMERGENCY` | Pet Care (`animal`), Medical (`hospital`) | Pet Care has search_order 12, Medical has 17 |
| `GROCERY OUTLET 0987` | Groceries (`grocery`), Other Shopping (`outlet`) | Groceries has search_order 7, Other Shopping has 999 |
| `AMAZON PRIME VIDEO` | Entertainment (`video`), Other Shopping (`amazon`) | Entertainment has search_order 20, Other Shopping has 999 |

These cases are covered by the test suite as a readable specification.

## Tests

```
pytest
```

run from the project root. Nine tests cover the categorizer's behavior, including the search_order edge cases above, case-insensitivity, and the various "no match" paths.

## Background

This project began as the final project for [Harvard's CS50P](https://cs50.harvard.edu/python/) in early 2024. The original submission already had the class architecture above (manager/controller separation, validating property setters, the search_order mechanism for categorization), but everything lived in a single ~1,300-line file. I subsequently refactored it into the modular structure shown above. The refactor split the code into one module per concern, extracted `categorize_item` from a method into a standalone pure function, added a `ui` abstraction layer so the managers no longer call `print()` directly, and grouped the launch flourish into its own `whimsy` module.

Development was eventually paused. The next logical step (improving the categorizer with LLM-based matching) would have required either an external API call, which is inappropriate for sensitive financial data, or self-hosting a local model, which was out of scope for what was meant to be a learning project. Stopping at this point felt like the right call: it leaves a self-contained, working application with cleanly demonstrable design choices, rather than an incomplete attempt at a different architecture.
