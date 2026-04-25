"""
Tests for the categorizer module.

Verifies that categorize_item correctly maps transaction descriptions to budget
categories using keyword matching, with priority resolved by search_order
(lower numbers checked first, ensuring the right category wins when multiple
keywords could match a single description).

Each test reads as a small specification of the module's intended behavior.
"""
import pytest

from budget_category import BudgetCategory
from categorizer import categorize_item


@pytest.fixture
def categories():
    """A small representative set of categories that exercises the search_order
    mechanism. The keywords and orders are chosen specifically to allow several
    descriptions to potentially match more than one category, so the tests can
    confirm that search_order resolves the conflict correctly."""
    return [
        BudgetCategory('Food & Dining', 'Groceries', 'safeway|grocery', '1', '0', '7'),
        BudgetCategory('Food & Dining', 'Eating Out', 'starbuck|chipotle', '2', '0', '8'),
        BudgetCategory('Health & Fitness', 'Medical', 'hospital|kaiser', '3', '0', '17'),
        BudgetCategory('Other', 'Pet Care', 'animal|vet|dog', '4', '0', '12'),
        BudgetCategory('Other', 'Entertainment', 'netflix|video', '5', '0', '20'),
        BudgetCategory('Shopping', 'Other Shopping', 'amazon|outlet|target', '6', '0', '999'),
    ]


def test_basic_match(categories):
    """A description containing a clear keyword returns the matching category."""
    assert categorize_item(categories, 'SAFEWAY 1234 SACRAMENTO') == 'Groceries'


def test_match_is_case_insensitive(categories):
    """Matching ignores case in both description and keyword."""
    assert categorize_item(categories, 'starbucks downtown') == 'Eating Out'
    assert categorize_item(categories, 'STARBUCKS DOWNTOWN') == 'Eating Out'
    assert categorize_item(categories, 'StArBuCks DoWnToWn') == 'Eating Out'


def test_search_order_pet_beats_medical(categories):
    """An 'animal hospital' description should match Pet Care (search_order 12)
    before Medical (search_order 17), even though 'hospital' is a Medical keyword."""
    assert categorize_item(categories, 'ANIMAL HOSPITAL EMERGENCY VISIT') == 'Pet Care'


def test_search_order_groceries_beats_other_shopping(categories):
    """A 'grocery outlet' description should match Groceries (search_order 7)
    before Other Shopping (search_order 999), even though 'outlet' is an
    Other Shopping keyword."""
    assert categorize_item(categories, 'GROCERY OUTLET 0987 SACRAMENTO') == 'Groceries'


def test_search_order_entertainment_beats_other_shopping(categories):
    """An 'amazon prime video' description should match Entertainment
    (search_order 20) before Other Shopping (search_order 999), because
    'video' is an Entertainment keyword."""
    assert categorize_item(categories, 'AMAZON PRIME VIDEO ONLINE') == 'Entertainment'


def test_no_match_returns_uncategorized(categories):
    """A description containing no recognized keywords returns 'Uncategorized'."""
    assert categorize_item(categories, 'CHECK # 1234') == 'Uncategorized'


def test_empty_description_returns_uncategorized(categories):
    """An empty description returns 'Uncategorized'."""
    assert categorize_item(categories, '') == 'Uncategorized'


def test_empty_categories_returns_uncategorized():
    """An empty category list returns 'Uncategorized' regardless of the description."""
    assert categorize_item([], 'SAFEWAY GROCERIES') == 'Uncategorized'


def test_first_keyword_in_category_wins(categories):
    """When a description matches multiple keywords from different categories,
    the category with the lower search_order is chosen — even if the higher-order
    category's keyword appears earlier in the description text."""
    # 'amazon' (Other Shopping, order 999) appears before 'video' (Entertainment, order 20)
    # but Entertainment should still win because of search_order.
    assert categorize_item(categories, 'amazon refund video purchase') == 'Entertainment'
