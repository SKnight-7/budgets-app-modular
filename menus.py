def generate_menu(menu_options, menu_title='MENU'):
    """
    Generates a formatted menu string based on the provided menu options.

    Args:
        menu_options (list): A list of dictionaries representing the menu options.
        menu_title (str): The title of the menu (default: 'MENU').

    Returns:
        str: The formatted menu string.
    """
    required_keys = ['general classification', 'option title', 'option number']

    for dictionary in menu_options:
        for key in required_keys:
            if key not in dictionary:
                return f"Unable to load menu. Please ensure your data contains the keys '{required_keys[0]}', '{required_keys[1]}' and '{required_keys[2]}', then try again."

    menu_to_display = [f"\n\n\x1B[4m{menu_title}\x1B[0m"]  # Start with underlined menu title

    current_classification = None  # We only want to print the overall classification when it changes
    # Sort by option number
    for item in sorted(menu_options, key=lambda x: int(x[required_keys[2]])):
        if item[required_keys[0]] != current_classification:  # Only add the category name if we have a new category
            menu_to_display.append(f"\n{item[required_keys[0]]}:")
            current_classification = item[required_keys[0]]
        # Add the subcategory with its option number
        menu_to_display.append(f"    {item[required_keys[2]]} - {item[required_keys[1]]}")
    # Insert a blank line to separate the menu from the user input request
    menu_to_display.append("")

    return '\n'.join(menu_to_display)

def initialize_budget_menu():
    """
    Initializes the budget menu display.

    Returns:
        str: String representation of the budget menu display.
    """
    budget_menu = "\nAVAILABLE CATEGORIES:\n\n"
    budget_menu += "\x1B[4mINCOME\x1B[0m             \x1B[4mMONTHLY HOUSEHOLD\x1B[0m      \x1B[4mFOOD & DINING\x1B[0m          \x1B[4mTRAVEL & TRANSPORT\x1B[0m\n"
    budget_menu += " 1: Paycheck        3: Mortgage & Rent     7: Groceries           9: Car (Payment, Gas, Repair,\n"
    budget_menu += " 2: Other Income    4: Utilities           8: Eating Out             Ride Share, Tolls, Parking)\n"
    budget_menu += "                    5: Phone                                     10: Public Transit\n"
    budget_menu += "                    6: Internet, Cable,                          11: Trips & Travel\n"
    budget_menu += "                       Satellite\n\n"
    budget_menu += "\x1B[4mHEALTH & FITNESS\x1B[0m   \x1B[4mFINANCIAL\x1B[0m              \x1B[4mSHOPPING\x1B[0m               \x1B[4mOTHER\x1B[0m\n"
    budget_menu += "12: Medical        14: Pay Loans &        15: Home Improvement   17: Self Care\n"
    budget_menu += "13: Gym & Other        Credit Cards       16: Other Shopping     18: Pet Care\n"
    budget_menu += "    Fitness                                                      19: Laundry\n"
    budget_menu += "                                                                 20: Entertainment"

    return budget_menu