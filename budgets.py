import csv
import os
import sys
import ui
from budget_category import BudgetCategory
from categorizer import categorize_item
from datetime import datetime
from default_categories import get_default_categories
from menus import generate_menu, initialize_budget_menu
from tabulate import tabulate
from transaction import Transaction

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_DIR = os.path.join(BASE_DIR, 'csv')


class BudgetManager:
    """
    Manages budget categories and performs budget-related operations.

    Attributes:
        budgets_csv_file (str): The internally created and managed CSV file storing the budget data (default: 'current_budgets.csv').
        budget_categories (dict): Dictionary mapping budget categories to BudgetCategory objects.
        budget_menu (str): String representation of the budget menu display.
        income_by_category (dict): Dictionary mapping income categories to their respective totals.
        expenditures_by_category (dict): Dictionary mapping expenditure categories to their respective totals.
    """

    def __init__(self, budgets_csv_file: str = 'current_budgets.csv'):
        """
        Initializes a BudgetManager object and sets the name of the internally created and managed CSV file for storing budget data.

        Args:
            budgets_csv_file (str): The CSV file name for storing budget data (default: 'current_budgets.csv').
        """
        self.budgets_csv_file = budgets_csv_file
        self.budgets_file_path = os.path.join(CSV_DIR, self.budgets_csv_file)

        # Dictionary with BudgetCategory objects as values, and their budget_category attribute as keys
        self.budget_categories = self.initialize_default_budget_categories()
        self.budget_menu = initialize_budget_menu() # String representation of menu display

        # Used to calculate expenditures by budget category
        self.income_by_category = {}
        self.expenditures_by_category = {'Uncategorized': 0}

        # Create two dictionaries with budget categories as keys and totals by budget category as values
        for category in self.budget_categories:
            if self.budget_categories[category].general_classification == 'Income':
                self.income_by_category[category] = 0
            else:
                self.expenditures_by_category[category] = 0

    def initialize_default_budget_categories(self):
        """
        Initializes the default budget categories. Takes a list of BudgetCategory objects,
        then makes those objects the values of the dictionary, with their own budget_category attributes as keys.

        Returns:
            dict: Dictionary mapping budget categories to BudgetCategory objects.
        """

        self.category_objects = get_default_categories()
        return {category_obj.budget_category: category_obj for category_obj in self.category_objects}

    @property
    def budgets_csv_file(self):
        """
        Getter method for the budgets_csv_file attribute.

        Returns:
            str: The CSV file storing the budget data.
        """
        return self._budgets_csv_file

    @budgets_csv_file.setter
    def budgets_csv_file(self, budgets_csv_file: str):
        """
        Setter method for the budgets_csv_file attribute.

        Args:
            budgets_csv_file (str): The CSV file to set for storing the budget data.

        Raises:
            ValueError: If the provided file is not of type CSV.
        """
        if not budgets_csv_file.endswith('.csv'):
            raise ValueError(f'File must be of type CSV')
        self._budgets_csv_file = budgets_csv_file

    @property
    def budget_categories(self):
        """
        Getter method for the budget_categories attribute.

        Returns:
            dict: Dictionary mapping budget categories to BudgetCategory objects.
        """
        return self._budget_categories

    @budget_categories.setter
    def budget_categories(self, budget_categories: dict):
        """
        Setter method for the budget_categories attribute.

        Args:
            budget_categories (dict): Dictionary mapping budget categories to BudgetCategory objects.

        Raises:
            TypeError: If the provided budget_categories is not a dictionary.
            ValueError: If any value in budget_categories is not a BudgetCategory instance.
        """
        if not isinstance(budget_categories, dict):
            raise TypeError("budget_categories must be a dictionary")
        if not all(isinstance(category, BudgetCategory) for category in budget_categories.values()):
            raise ValueError("All values in budget_categories must be BudgetCategory instances")
        self._budget_categories = budget_categories

    @property
    def expenditures_by_category(self):
        """
        Getter method for the expenditures_by_category attribute.

        Returns:
            dict: Dictionary mapping expenditure categories to their respective totals.
        """
        return self._expenditures_by_category

    @expenditures_by_category.setter
    def expenditures_by_category(self, expenditures_by_category):
        """
        Setter method for the expenditures_by_category attribute.

        Args:
            expenditures_by_category (dict): Dictionary mapping expenditure categories to their respective totals.

        Raises:
            TypeError: If the provided expenditures_by_category is not a dictionary.
            ValueError: If any key in expenditures_by_category is not a string or any value is not a number.
        """
        if not isinstance(expenditures_by_category, dict):
            raise TypeError("expenditures_by_category must be a dictionary")
        if not all(isinstance(k, str) and isinstance(v, (int, float)) for k, v in expenditures_by_category.items()):
            raise ValueError(
                "All keys in expenditures_by_category must be strings and all values must be numbers")
        self._expenditures_by_category = expenditures_by_category

    @property
    def income_by_category(self):
        """
        Getter method for the income_by_category attribute.

        Returns:
            dict: Dictionary mapping income categories to their respective totals.
        """
        return self._income_by_category

    @income_by_category.setter
    def income_by_category(self, income_by_category):
        """
        Setter method for the income_by_category attribute.

        Args:
            income_by_category (dict): Dictionary mapping income categories to their respective totals.

        Raises:
            TypeError: If the provided income_by_category is not a dictionary.
            ValueError: If any key in income_by_category is not a string or any value is not a number.
        """
        if not isinstance(income_by_category, dict):
            raise TypeError("expenditures_by_category must be a dictionary")
        if not all(isinstance(k, str) and isinstance(v, (int, float)) for k, v in income_by_category.items()):
            raise ValueError(
                "All keys in expenditures_by_category must be strings and all values must be numbers")
        self._income_by_category = income_by_category

    def __str__(self):
        """
        Returns a string representation of the BudgetManager object.
        Creates a list of strings consisting of available budget categories with their budgeted amounts
        Then joins the strings in the list into one string with the items displayed on their own lines.

        Returns:
            str: The string representation of the BudgetManager object that shows the name of the file used for
            storing budget data and the amounts budgeted by category.
        """
        categories_and_amounts = '\n'.join([f"{category}: ${obj.amt_budgeted}" for category, obj in self.budget_categories.items()])
        return f"Internal data storage file: {self.budgets_csv_file}\nCurrent budgets:\n{categories_and_amounts}"

    def get_stored_budgets(self):
        """
        Reads in the stored budget data from the CSV file.
        If the file doesn't exist, initializes it with default data.
        """

        if not os.path.exists(self.budgets_file_path):
            self.update_stored_budgets()  # Initialize the file with default data
        else:
            with open(self.budgets_file_path, 'r', newline='') as file:
                reader = csv.DictReader(file)
                self.budget_categories = {}  # Prepare to load categories from file
                for row in reader:
                    self.budget_categories[row['budget_category']] = BudgetCategory(
                        row['general_classification'],
                        row['budget_category'],
                        row['keywords'],
                        row['option_num'],
                        row['amt_budgeted'],
                        row['search_order'])

    def get_budget_category_to_update(self):
        """
        Prompts the user to enter the option number of the budget category to update or 'q' to exit.

        Returns:
            str: The selected budget category or 'q' if the user chooses to exit.
            None: If the user enters an invalid option number.
        """
        try:
            selection = ui.get_option_number("Enter option number of selected budget category or 'q' to exit: ")
        except EOFError:
            sys.exit("Goodbye!")  # Assume EOFError indicates user wants to quit out of program
        if selection.lower() == 'q':
            return 'q'  # Lets calling function know user wants to quit out of current menu
        try:
            for category in self.budget_categories.values():
                if int(selection) == category.option_num:
                    return category.budget_category
        except ValueError:
            return None

    def get_new_budget_amt(self, category):
        """
        Prompts the user to enter a new budget amount for the specified category or 'q' to choose a different category.

        Args:
            category (str): The budget category to update.

        Returns:
            float: The new budget amount entered by the user.
            'q': If the user chooses to quit out of the current menu.
            None: If the user enters an invalid budget amount.
        """
        proposed_budget_amount = ui.get_user_input(
            f"Please enter a budget amount for {category} in the format #####.## or 'q' to choose a different category:\n")
        if proposed_budget_amount.lower() == 'q':
            return 'q'  # Lets calling function know user wants to quit out of current menu
        try:  # Ensure amount is a number
            new_budget = round(float(proposed_budget_amount), 2)
        except (ValueError, TypeError):
            return None
        return new_budget

    def update_budget_amount(self):
        """
        Prompts the user to update the budget amount for a selected budget category.
        Displays the updated budgets with expenditures after the update.
        """
        while True:
            ui.display_budget_menu(f"{self.budget_menu}\n\nPlease select a budget to update. To delete a budget, please update the budgeted amount to 0")
            # Gets the key in the self.budget_categories dictionary
            category_to_update = self.get_budget_category_to_update()
            if category_to_update is None:
                # Let the user know their selection was invalid before reprompting
                ui.display_error("Invalid option, please try again.")
                continue
            if category_to_update == 'q':
                return 'q'  # Lets calling function know user wants to quit out of budget menu
            while True:
                new_budget_amt = self.get_new_budget_amt(category_to_update)
                if new_budget_amt is None:
                    ui.display_error('Invalid entry')
                    continue  # Let user try entering the budget amount again, in case they just used the wrong format or miskeyed the input
                if new_budget_amt == 'q':   # If user enters 'q' instead of an amount, they may have meant to choose a different category
                    break
                if new_budget_amt < 0:  # Validate user input as positive or zero
                    ui.display_error("Budget amount must be 0.00 or greater")
                    continue
                self.budget_categories[category_to_update].amt_budgeted = new_budget_amt
                self.update_stored_budgets()
                ui.display_budgets(self.format_budgets_with_expenditures())
                break

    def update_stored_budgets(self):
        """
        Updates the stored budget data in the CSV file with the current budget data.
        Overwrites whatever was in the file with the data currently in memory.
        """
        with open(self.budgets_file_path, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=[
                                    'general_classification', 'budget_category', 'keywords', 'option_num', 'amt_budgeted', 'search_order'])
            writer.writeheader()
            for category_obj in self.budget_categories.values():
                writer.writerow({
                    'general_classification': category_obj.general_classification,
                    'budget_category': category_obj.budget_category,
                    'keywords': '|'.join(category_obj.keywords),
                    'option_num': str(category_obj.option_num),
                    'amt_budgeted': f"{category_obj.amt_budgeted:.2f}",
                    'search_order': str(category_obj.search_order)
                })

    def format_budgets_with_expenditures(self, transactions_source=None):
        """
        Formats the budgets with expenditures for display.

        Args:
            transactions_source (str): The filename from which this collection of transactions was originally uploaded by the user (default: None).

        Returns:
            str: The formatted string representing the budgets with expenditures.
        """
        # Initialize headers and lists for income and expenditures
        income_headers = ['Income Category', 'Expected', 'Received', 'Pending']
        expenditures_headers = ['Budget Category', 'Budgeted', 'Expended', 'Remaining']
        income_data, expenditures_data = [], []

        # Initialize totals
        total_expected_income, total_budgeted_expenses, total_received, total_expended = 0, 0, 0, 0

        # Process each budget category
        for category in self.budget_categories.values():
            if category.general_classification == 'Income':
                received = self.income_by_category.get(category.budget_category, 0)
                pending = category.amt_budgeted - received
                if category.amt_budgeted != 0 or received != 0:
                    total_expected_income += category.amt_budgeted
                    total_received += received
                    income_data.append(
                        [category.budget_category, category.amt_budgeted, received, pending])
            else:
                expended = self.expenditures_by_category.get(category.budget_category, 0)
                remaining = category.amt_budgeted - expended
                if category.amt_budgeted != 0 or expended != 0:
                    total_budgeted_expenses += category.amt_budgeted
                    total_expended += expended
                    expenditures_data.append(
                        [category.budget_category, category.amt_budgeted, expended, remaining])

        if not income_data and not expenditures_data:
            return "\nThere are no budgets to display.\n"

        # Calculate available to allocate and unspent balance
        available_to_allocate = total_expected_income - total_budgeted_expenses
        unspent_balance = total_budgeted_expenses - total_expended

        # Format the data for display using tabulate
        income_table = tabulate(income_data, headers=income_headers, tablefmt="grid", floatfmt=',.2f')
        expenditures_table = tabulate(expenditures_data, headers=expenditures_headers, tablefmt="grid", floatfmt=',.2f')

        # Build the display string
        header = f"\n\n\x1B[4mYOUR CURRENT BUDGETS\x1B[0m\nBased on transactions from: {transactions_source if transactions_source else 'N/A'}"

        income_section = f"{income_table}\nTotal Expected Income: ${total_expected_income:,.2f}\nTotal Received: ${total_received:,.2f}\nAvailable to allocate: ${available_to_allocate:,.2f}"
        expenditure_section = f"{expenditures_table}\nUncategorized: ${self.expenditures_by_category.get('Uncategorized', 0):,.2f}\n\nTotal Budgeted: ${total_budgeted_expenses:,.2f}\nTotal Expended: ${total_expended:,.2f}\nUnspent balance: ${unspent_balance:,.2f}"

        # Concatenate all the sections into the final display string
        return f"{header}\n\n{income_section}\n\n{expenditure_section}"

class TransactionsManager:
    """
    Manages financial transactions and performs transaction-related operations.

    Attributes:
        source_file (str): The name of the user-provided CSV file from which this collection of transactions was uploaded (default: 'sample.csv').
        transactions_csv_file (str): The name of the internally created and managed CSV file storing the transaction data (default: 'last_uploaded_transactions.csv').
        transactions (dict): Dictionary mapping transaction numbers to Transaction objects.
    """
    def __init__(self, source_file='sample.csv', transactions_csv_file='last_uploaded_transactions.csv'):
        """
        Initializes a TransactionsManager object with the provided source file and transactions CSV file.

        Args:
            source_file (str): The name of the user-provided CSV file from which this collection of transactions was uploaded (default: 'sample.csv').
            transactions_csv_file (str): The name of the internally created and managed CSV file storing the transaction data (default: 'last_uploaded_transactions.csv').
        """
        self.source_file = source_file
        self.transactions_csv_file = transactions_csv_file
        
        # Set up full file paths
        self.source_file_path = os.path.join(CSV_DIR, self.source_file)
        self.transactions_file_path = os.path.join(CSV_DIR, self.transactions_csv_file)

        # Dictionary with BudgetCategory objects as values, and their budget_category attribute as keys
        self.transactions = self.make_transactions_dictionary()

    def make_transactions_dictionary(self, transaction_objects=[Transaction('0', '1900-01-01', '0', 'Sample', 'Uncategorized', 'sample.csv')]):
        """
        Creates a dictionary mapping transaction numbers to Transaction objects.

        Args:
            transaction_objects (list): List of Transaction objects (default: [Transaction('0', '1900-01-01', '0', 'Sample', 'Uncategorized', 'sample.csv')]).

        Returns:
            dict: Dictionary mapping transaction numbers to Transaction objects.
        """
        self.transaction_objects = transaction_objects
        return {transaction_obj.transaction_num: transaction_obj for transaction_obj in self.transaction_objects}

    @property
    def source_file(self):
        """
        Getter method for the source_file attribute.

        Returns:
            str: The name of the user-provided CSV file from which this collection of transactions was uploaded.
        """
        return self._source_file

    @source_file.setter
    def source_file(self, source_file: str):
        """
        Setter method for the source_file attribute.

        Args:
            source_file (str): The source file to set for the transactions.

        Raises:
            ValueError: If the provided source file is not of type CSV.
        """
        if not source_file.endswith('.csv'):
            raise ValueError(f'File must be of type CSV')
        self._source_file = source_file

    @property
    def transactions_csv_file(self):
        """
        Getter method for the transactions_csv_file attribute.

        Returns:
            str: The name of the internally created and managed CSV file storing the transaction data.
        """
        return self._transactions_csv_file

    @transactions_csv_file.setter
    def transactions_csv_file(self, transactions_csv_file: str):
        """
        Setter method for the transactions_csv_file attribute.

        Args:
            transactions_csv_file (str): The name of the CSV file to set for storing the transaction data.

        Raises:
            ValueError: If the provided file is not of type CSV.
        """
        if not transactions_csv_file.endswith('.csv'):
            raise ValueError(f'File must be of type CSV')
        self._transactions_csv_file = transactions_csv_file

    @property
    def transactions(self):
        """
        Getter method for the transactions attribute.

        Returns:
            dict: Dictionary mapping transaction numbers to Transaction objects.
        """
        return self._transactions

    @transactions.setter
    def transactions(self, transactions: dict):
        """
        Setter method for the transactions attribute.

        Args:
            transactions (dict): Dictionary mapping transaction numbers to Transaction objects.

        Raises:
            TypeError: If the provided transactions is not a dictionary.
            ValueError: If any value in transactions is not a Transaction instance.
        """
        if not isinstance(transactions, dict):
            raise TypeError("Collection of transactions must be a dictionary")
        if not all(isinstance(transaction, Transaction) for transaction in transactions.values()):
            raise ValueError("All values in budget_categories must be BudgetCategory instances")
        self._transactions = transactions

    def __str__(self):
        """
        Returns a string representation of the TransactionsManager object as labeled data such as
        the internally created and managed CSV file name used for storing transactions data,
        the user-uploaded CSV file name from which this collection of transactions came,
        the number of transactions in this collection, and the number of transactions by budget category.

        Returns:
            str: The string representation of the TransactionsManager object.
        """
        total_transactions = len(self.transactions)
        transactions_by_category = {}
        for transaction in self.transactions.values():
            if transaction.category in transactions_by_category:
                transactions_by_category[transaction.category] += 1
            else:
                transactions_by_category[transaction.category] = 1

        output = f"Internal data storage file: {self.transactions_csv_file}\n"
        output += f"Last uploaded transactions: {self.source_file}\n"
        output += f"Total transactions: {total_transactions}\n"
        output += "Transactions by category:\n"
        for category, count in transactions_by_category.items():
            output += f"{category}: {count} transactions\n"

        return output

    def get_stored_transactions(self):
        """
        Reads in the stored transaction data from the CSV file. Since the transaction number isn't coming
        directly from the Transaction object, whose setters will transform the data to an int,
        manually transforms the transaction number from a numerical string to an integer.
        If the file doesn't exist, initializes it with default data.
        """
        if not os.path.exists(self.transactions_file_path):
            self.update_stored_transactions()  # Initialize the file with default data
        else:
            source_files_in_data = []
            with open(self.transactions_file_path, 'r', newline='') as file:
                reader = csv.DictReader(file)
                self.transactions = {}  # Prepare to load transactions from file
                for row in reader:
                    self.transactions[int(row['transaction_num'])] = Transaction(
                        row['transaction_num'],
                        row['transaction_date'],
                        row['amount'],
                        row['description'],
                        row['category'],
                        row['source_file'])
                    if row['source_file'] not in source_files_in_data:
                        source_files_in_data.append(row['source_file'])
            self.source_file = ', '.join(source_files_in_data)

    def update_stored_transactions(self):
        """
        Updates the stored transaction data in the CSV file with the current transactions.
        Overwrites whatever was in the file with the data currently in memory.
        """
        with open(self.transactions_file_path, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=[
                                    'transaction_num', 'transaction_date', 'amount', 'description', 'category', 'source_file'])
            writer.writeheader()
            for transaction_obj in self.transactions.values():
                writer.writerow({
                    'transaction_num': str(transaction_obj.transaction_num),
                    'transaction_date': transaction_obj.transaction_date.strftime('%Y-%m-%d'),
                    'amount': f"{transaction_obj.amount:.2f}",
                    'description': transaction_obj.description,
                    'category': transaction_obj.category,
                    'source_file': transaction_obj.source_file})

    def load_user_transactions(self):
        """
        Loads user transactions from the source file. Expects a CSV file in the project folder that was downloaded from the user's bank and
        contains transactions information. Designed based on Wells Fargo CSV files, which contain the following columns (no headers):
        date, amount, asterisk, blank or check number, description.

        Returns:
            bool: True if the transactions were loaded successfully, False otherwise.
        """
        self.source_file_path=os.path.join(CSV_DIR,self.source_file)
        try:
            with open(self.source_file_path, 'r', newline='') as file:
                reader = csv.reader(file)
                self.transactions = {} # Prepare to load transactions from file
                i = 0
                for i, row in enumerate(reader, start=1):
                    self.transactions[i] = Transaction(
                        i, # Transaction number
                        datetime.strptime(row[0], '%m/%d/%Y').strftime('%Y-%m-%d'), # Date (reformatted)
                        row[1], # Amount
                        row[4] if len(row) >= 5 else "", # Description
                        'Uncategorized',
                        self.source_file)
        except (FileNotFoundError, IndexError, csv.Error):
            return False
        self.update_stored_transactions() # Stores initial data
        return True

    def get_transaction_to_update(self):
        """
        Prompts the user to enter a transaction number to update or 'q' to exit.

        Returns:
            int: The transaction number to update.
            'q': If the user chooses to quit out of the current menu.
            None: If the user enters an invalid transaction number.
        """
        try:
            selection = ui.get_option_number("Enter transaction number or 'q' to exit: ")
        except EOFError:
            sys.exit("Goodbye!")  # Assume EOFError indicates user wants to quit out of program
        if selection.lower() == 'q':
            return 'q'  # Lets calling function know user wants to quit out of current menu
        try:
            selection = int(selection)
            if selection not in self.transactions:
                raise ValueError
        except ValueError:
            return None
        return selection

    def formatted_transactions(self, sorted_by='Transaction number', ascending=True):
        """
        Formats the transactions for display, sorted by the specified criteria.

        Args:
            sorted_by (str): The criteria to sort the transactions by (default: 'Transaction number').
            ascending (bool): Whether to sort in ascending order (default: True).

        Returns:
            str: The formatted string representing the transactions.
         """
        match sorted_by:
            case 'Transaction number':
                sort_key = lambda x: x.transaction_num
            case 'Transaction date':
                sort_key = lambda x: x.transaction_date
            case 'Amount':
                sort_key = lambda x: x.amount
            case 'Category':
                sort_key = lambda x: x.category
            case _:
                ui.display_error(f"Cannot sort by {sorted_by}")
                sort_key = lambda x: x.transaction_num

        sorted_transactions = sorted(self.transactions.values(), key=sort_key, reverse=not ascending) # Sorted function returns a list

        transactions_for_display = [{
            'Transaction #': transaction.transaction_num,
            'Date': transaction.transaction_date.strftime('%Y-%m-%d'),
            'Amount': f"{transaction.amount:,.2f}",
            'Description': transaction.description,
            'Category': transaction.category
        } for transaction in sorted_transactions]

        # Use tabulate to format the transactions for display
        display = tabulate(transactions_for_display, headers='keys', tablefmt='grid', floatfmt=".2f")
        return f"\n\n\x1B[4mLAST UPLOADED TRANSACTIONS\x1B[0m\nTransactions from: {self.source_file}\n\n{display}"


class FinancialController:
    """
    Controls financial operations by managing budgets and transactions.

    Attributes:
        budget_manager (BudgetManager): The budget manager object.
        transactions_manager (TransactionsManager): The transactions manager object.
    """
    def __init__(self):
        """
        Initializes a FinancialController object and loads the most recent budgets and transactions data into memory.
        """
        self.budget_manager = BudgetManager()
        self.transactions_manager = TransactionsManager()

        # Load most recent data into memory
        self.budget_manager.get_stored_budgets()
        self.transactions_manager.get_stored_transactions()

        self.categories = get_default_categories()

    def calculate_totals_by_category(self):
        """
        Calculates the totals for income and expenditures by category.
        """
        self.budget_manager.income_by_category = {category: 0.0 for category in self.budget_manager.income_by_category}
        self.budget_manager.expenditures_by_category = {category: 0.0 for category in self.budget_manager.expenditures_by_category}

        # Bank CSV files treat transactions coming into the account as positive, and transactions going out of the account as negative.
        # Switch the signs of expenditures to display as positive amounts
        for transaction in self.transactions_manager.transactions.values():
            if transaction.category in self.budget_manager.income_by_category:
                self.budget_manager.income_by_category[transaction.category] += transaction.amount
            elif transaction.category in self.budget_manager.expenditures_by_category:
                self.budget_manager.expenditures_by_category[transaction.category] -= transaction.amount
            else:
                self.budget_manager.expenditures_by_category['Uncategorized'] -= transaction.amount

    def view_current_budgets(self):
        """
        Calculates the totals by category and returns the formatted budgets with expenditures.

        Returns:
            str: The formatted string representing the current budgets with expenditures.
        """
        self.calculate_totals_by_category()
        return self.budget_manager.format_budgets_with_expenditures(self.transactions_manager.source_file)

    def update_budgets(self):
        """
        Calls the BudgetManager method, ensuring main() interacts solely with the FinancialController, not directly with the other classes.
        Updates the budget amounts through user interaction.
        """
        self.budget_manager.update_budget_amount()

    def categorize_all_transactions(self):
        """
        Categorizes all transactions based on their descriptions.
        """
        for transaction in self.transactions_manager.transactions.values():
            category = categorize_item(self.categories, transaction.description)
            transaction.category = category

    def process_user_transactions(self, user_filename):
        """
        Processes user transactions from the specified file: Stores the file name in the TransactionsManager object,
        reads in the data, categorizes each transaction, updates the internal CSV file that stores transactions data,
        and calculates total income and expenditures by budget category.

        Args:
            user_filename (str): The name of the file containing user transactions.

        Returns:
            bool: True if the transactions were processed successfully, False otherwise.
        """
        self.transactions_manager.source_file = user_filename
        if not self.transactions_manager.load_user_transactions(): # Try to load user transactions into memory
            return False
        self.categorize_all_transactions()
        self.transactions_manager.update_stored_transactions()
        self.calculate_totals_by_category()
        return True

    def format_transactions(self, sort_by='Transaction number', ascending=True):
        """
        Calls the TransactionsManager method, ensuring main() interacts solely with the FinancialController,
        not directly with the other classes. Formats the transactions for display, sorted by the specified criteria.

        Args:
            sort_by (str): The criteria to sort the transactions by (default: 'Transaction number').
            ascending (bool): Whether to sort in ascending order (default: True).

        Returns:
            str: The formatted string representing the transactions.
        """
        return self.transactions_manager.formatted_transactions(sort_by, ascending)

    def recategorize_transactions(self, sort_order='Category'):
        """
        Allows the user to recategorize transactions through user interaction.
        Process: Transactions by category are displayed. When the user selects a transaction number to reclassify, the budget categories
        are displayed. When the user selects a budget category by option number, the chosen transaction is reclassified to that budget category.
        Changes to both the transactions and the budgets with expenditures that result from recategorization are displayed, and the user can
        select another transaction number to recategorize. The process continues until the user enters 'q'.

        Args:
            sort_order (str): The order in which to sort the transactions for display (default: 'Category').

        Returns:
            str: 'q' if the user chooses to quit out of the current menu.
        """
        while True:
            ui.display_transactions(self.transactions_manager.formatted_transactions(sort_order))
            # Gets and validates transaction number
            transaction_to_update = self.transactions_manager.get_transaction_to_update()
            if transaction_to_update is None:
                # Let the user know their selection was invalid before reprompting
                ui.display_error("Invalid transaction number. Please try again.")
                continue
            if transaction_to_update == 'q':
                return 'q'  # Lets calling function know user wants to quit out of current menu
            while True:
                ui.display_budget_menu(self.budget_manager.budget_menu)
                new_category = self.budget_manager.get_budget_category_to_update()
                if new_category is None:
                    ui.display_error('Please select from the available categories')
                    continue  # Let user try entering the category again, in case they just miskeyed the input
                if new_category == 'q':   # If user enters 'q' instead of an amount, they may have meant to choose a different transaction
                    break
                self.transactions_manager.transactions[transaction_to_update].category = new_category
                self.transactions_manager.update_stored_transactions()
                self.calculate_totals_by_category()
                ui.display_budgets(self.budget_manager.format_budgets_with_expenditures(self.transactions_manager.source_file))
                break

MAIN_MENU = [
    {'general classification': 'Budget Options',
        'option title': 'View current budgets',
        'option number': '1',
        },
    {'general classification': 'Budget Options',
        'option title': 'Update budgets',
        'option number': '2',
        },
    {'general classification': 'Transaction Options',
        'option title': 'Choose a CSV transaction file to load',
        'option number': '3',
        },
    {'general classification': 'Transaction Options',
        'option title': 'View transactions by category',
        'option number': '4',
        },
    {'general classification': 'Transaction Options',
        'option title': 'View transactions in original order',
        'option number': '5',
        },
    {'general classification': 'Transaction Options',
        'option title': 'Recategorize transactions',
        'option number': '6',
        }]

def main():
    """
    The main function that runs the financial management program.
    """
    controller = FinancialController()

    ui.display_whimsy(True)

    while True:
        ui.display_main_menu(generate_menu(MAIN_MENU, "MAIN MENU"))
        try:
            selection = ui.get_option_number("Please enter option number or 'q' to exit: ")
            if selection.lower() == 'q':
                raise EOFError  # Treat both EOF characters and 'q' as simple exit requests without needing to differentiate between them
        except EOFError:
            sys.exit("Goodbye!")

        match selection:
            case '1':  # View current budgets
                ui.display_budgets(controller.view_current_budgets())
            case '2':  # Update budgets
                ui.display_budgets(controller.view_current_budgets())
                controller.update_budgets()
            case '3':  # Choose a CSV transaction file to load
                instructions = "Please enter the name of a CSV file located in this project folder or 'q' to return to main menu."               
                ui.display_message(instructions)
                while True:
                    proposed_file = ui.get_filename("Filename: ")
                    if proposed_file.lower() == 'q':
                        break
                    if not proposed_file.endswith('.csv'):
                        proposed_file += '.csv'
                    if not os.path.exists(os.path.join(CSV_DIR, proposed_file)):
                        ui.display_error(f"The file '{proposed_file}' is invalid. Please try again, or enter 'q' to return to main menu:")
                        continue
                    break
                valid_file = proposed_file
                if valid_file.lower() == 'q':
                    continue
                if not controller.process_user_transactions(valid_file):
                    ui.display_error("There was a problem uploading the data. Please try again or select a different file uploaded to the project folder.")
                    continue
                ui.display_budgets(controller.view_current_budgets())
            case '4':  # View transactions by category
                ui.display_transactions(controller.format_transactions('Category'))
            case '5':  # View transactions in original order
                ui.display_transactions(controller.format_transactions('Transaction number'))
            case '6':  # Recategorize transactions
                controller.recategorize_transactions()
            case _:
                # Let the user know their selection was invalid before reprompting
                ui.display_error("Invalid option, please try again.")


if __name__ == '__main__':
    main()
