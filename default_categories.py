"""
This module defines the default budget categories for the financial management system.

It provides a function to retrieve a list of predefined BudgetCategory objects,
each representing a common budget category with associated keywords for transaction categorization.
These default categories serve as a starting point for users of the financial management system,
covering common income sources and expense categories.

The categories are organized with a specific search order to ensure accurate categorization
when dealing with potentially overlapping keywords across different categories.
"""

from budget_category import BudgetCategory

def get_default_categories():
    """
    Creates and returns a list of default BudgetCategory objects.

    This function defines a set of common budget categories, each with:
    - A general classification (e.g., 'Income', 'Monthly Household Bills')
    - A specific budget category name
    - Associated keywords for transaction categorization
    - An option number for user interface purposes
    - An initial budgeted amount (set to '0')
    - A search order for prioritizing categories during the categorization process

    The categories cover various aspects of personal finance, including income sources,
    household expenses, food and dining, transportation, health and fitness, financial obligations,
    shopping, and other miscellaneous expenses.

    Returns:
        list: A list of BudgetCategory objects representing the default budget categories.

    Example:
        >>> default_categories = get_default_categories()
        >>> len(default_categories)
        20
        >>> default_categories[0].budget_category
        'Paycheck'
        >>> default_categories[-1].keywords
        ['netflix', 'hulu', 'disney', 'video', 'spotify', 'audible', 'cinemark', 'amc', 'theater', 'theatre', 'playstation', 'nintendo', 'xbox', 'steam', 'nexus mods', 'game', 'subscription', 'youtube', 'channel', 'television', 'tv']
    """
    return [
        BudgetCategory('Income', 'Paycheck', 'payroll', '1', '0', '1'),
        BudgetCategory('Income', 'Other Income', 'cashout', '2', '0', '2'),
        BudgetCategory('Monthly Household Bills', 'Mortgage & Rent',
                        'apartments|mortgage', '3', '0', '3'),
        BudgetCategory('Monthly Household Bills', 'Utilities',
                        'utility|gas|electric|water|smud|pge', '4', '0', '4'),
        BudgetCategory('Monthly Household Bills', 'Phone',
                        'verizon|metropcs|mobile', '5', '0', '5'),
        BudgetCategory('Monthly Household Bills', 'Internet, Cable, Satellite',
                        'internet|comcast|xfinity|at&t|cable|satellite', '6', '0', '6'),
        BudgetCategory('Food & Dining', 'Groceries',
                        'safeway|kroger|aldi|publix|meijer|piggly|albertson|costco|trader joe|co-op|food|market|grocery', '7', '0', '7'),
        BudgetCategory('Food & Dining', 'Eating Out',
                        'mcdonald|starbuck|peets|chipotle|subway|panera|dunkin|taco|pizza|wings|burger|steak|coffee|yogurt', '8', '0', '8'),
        BudgetCategory('Travel & Transport', 'Car (Payment, Gas, Repair, Ride Share, Tolls, Parking)',
                        'dealership|auto|uber|lyft|toll|parking|shell|chevron|exxonmobil|bp|gas', '9', '0', '9'),
        BudgetCategory('Travel & Transport', 'Public Transit',
                        'transit| rt ', '10', '0', '10'),
        BudgetCategory('Travel & Transport', 'Trips & Travel',
                        'hotel|motel|airline', '11', '0', '14'),
        BudgetCategory('Health & Fitness', 'Medical',
                        'hospital|doctor|kaiser|medical|insurance|wellness|pharm|rx', '12', '0', '17'),
        BudgetCategory('Health & Fitness', 'Gym & Other Fitness',
                        'fitness|gym|pilates|dance|running', '13', '0', '13'),
        BudgetCategory('Financial', 'Pay Loans & Credit Cards',
                        'bank|loan|capital one|merrick|hsbc|american express|visa|mastercard|student ln|synchrony| cc ', '14', '0', '11'),
        BudgetCategory('Shopping', 'Home Improvement', 'lowe|home|hardware', '15', '0', '15'),
        BudgetCategory('Shopping', 'Other Shopping',
                        'amazon|amzn|ebay|macy|nordstrom|target|walmart|outlet|google', '16', '0', '999'),
        BudgetCategory('Other', 'Self Care',
                        'spa | hair|nail|salon|barber|massage|beauty', '17', '0', '17'),
        BudgetCategory('Other', 'Pet Care',
                        'chewy|animal|vet|kitty|cat |dog|hound|pup', '18', '0', '12'),
        BudgetCategory('Other', 'Laundry', 'csc', '19', '0', '19'),
        BudgetCategory('Other', 'Entertainment',
                        'netflix|hulu|disney|video|spotify|audible|cinemark|amc|theater|theatre|playstation|nintendo|xbox|steam|nexus mods|game|subscription|youtube|channel|television|tv',
                        '20', '0', '20'),
    ]

# Note: The search order (last parameter in each BudgetCategory) is crucial for the categorization process.
# Categories with more specific keywords or that should take precedence are given lower search order numbers.
# For example, 'Pet Care' (search order 12) is checked before 'Medical' (search order 17) to ensure
# that "pet hospital" is correctly categorized as 'Pet Care' rather than 'Medical'
