from whimsy import apply_whimsy

def display_message(message: str):
    """Generic function to display a message."""
    print(message)

def display_budgets(formatted_budgets) -> str:
    """Display the current budgets in a table."""
    print(formatted_budgets)

def display_transactions(formatted_transactions) -> str:
    """Display the last uploaded transactions."""
    print(formatted_transactions)

def display_whimsy(enable_whimsy=True):
    """Display the whimsical intro."""
    whimsical_content = apply_whimsy(enable_whimsy)
    print(whimsical_content)

def display_main_menu(menu):
    """Display the main menu."""
    print(menu)

def display_budget_menu(menu_and_instructions):
    """Display the budget menu."""
    print(menu_and_instructions)

def display_error(message: str):
    """Display an error message."""
    print(message)

def get_user_input(prompt: str) -> str:
    """Generic function to get user input."""
    return input(prompt)

def get_option_number(prompt: str) -> str:
    """Get the user's menu option selection."""
    return input(prompt)

def get_filename(prompt: str) -> str:
    """Get a filename from the user."""
    return input(prompt)
