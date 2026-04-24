"""
This module provides functionality for categorizing financial transactions based on their descriptions.

The main function, categorize_item, takes a list of BudgetCategory objects and a transaction description,
and returns the appropriate budget category based on keyword matching.

This module is part of a larger financial management system and works in conjunction with other modules
such as budget_category and transaction to provide a comprehensive budgeting and transaction categorization solution.
"""
from typing import List
from budget_category import BudgetCategory

def categorize_item(categories: List[BudgetCategory], item_description: str) -> str:
    """
    Categorizes a financial transaction based on its description.

    This function iterates through a list of BudgetCategory objects, each containing keywords.
    It checks if any of these keywords are present in the given item description.
    The categories are checked in order of their search_order attribute to ensure correct categorization
    in cases where keywords might overlap between categories.

    Args:
        categories (List[BudgetCategory]): A list of BudgetCategory objects, each representing a budget category
                                           and containing relevant keywords for that category.
        item_description (str): The description of the financial transaction to be categorized.

    Returns:
        str: The name of the budget category that matches the item description.
             If no match is found, returns 'Uncategorized'.

    Example:
        >>> categories = [BudgetCategory('Food', 'Groceries', 'supermarket|grocery', '1', '0', '1'),
        ...               BudgetCategory('Transport', 'Gas', 'shell|exxon', '2', '0', '2')]
        >>> categorize_item(categories, "Payment to Shell Gas Station")
        'Gas'
        >>> categorize_item(categories, "Amazon.com purchase")
        'Uncategorized'
    """
    for category in sorted(categories, key=lambda x: x.search_order):
        for keyword in category.keywords:
            if keyword.lower() in item_description.lower():
                return category.budget_category
    return 'Uncategorized'

# Note: The categorization process uses case-insensitive keyword matching.
# The search_order of categories is crucial for correct categorization in cases of overlapping keywords.
# For example, 'pet hospital' should match 'Pet Care' before 'Medical' if 'Pet Care' has a lower search_order.