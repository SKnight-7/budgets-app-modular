class BudgetCategory:
    """
    Represents a budget category with its associated attributes. BudgetCategory objects are expected to be created and modified
    either by reading in data from a CSV file or via user input. Since both of these methods provide data as strings,
    class attributes are correctly typed by the class setters to ensure consistency.

    Search order is used to prevent miscategorization. For example, 'animal hospital' should be mapped to Pet Care, not Medical,
    so pet care is searched first. Also, any outlets (such as 'grocery outlet') should be checked for other keywords
    before being mapped to shopping due to 'outlet', and 'amazon prime video' should be mapped to Entertainment due to 'video'
    before being mapped to Other Shopping due to 'amazon', so shopping should be searched last.

    Attributes:
        general_classification (str): The general classification of the budget category.
        budget_category (str): The name of the budget category.
        keywords (str): Keywords associated with the budget category, separated by '|'.
        option_num (str): The option number of the budget category.
        amt_budgeted (str): The amount budgeted for the category.
        search_order (str): The search order of the budget category.
    """

    def __init__(self, general_classification: str, budget_category: str, keywords: str, option_num: str, amt_budgeted: str, search_order: str):
        """
        Initializes a BudgetCategory object with the provided attributes.

        Args:
            general_classification (str): The general classification of the budget category.
            budget_category (str): The name of the budget category.
            keywords (str): Keywords associated with the budget category, separated by '|'.
            option_num (str): The option number of the budget category.
            amt_budgeted (str): The amount budgeted for the category.
            search_order (str): The search order of the budget category.
        """
        self.general_classification = general_classification
        self.budget_category = budget_category
        self.keywords = keywords
        self.option_num = option_num
        self.amt_budgeted = amt_budgeted
        self.search_order = search_order

    def __str__(self):
        """
        Returns a string representation of the BudgetCategory object's attributes as stored in memory.
        Keywords are stored in memory as a list, option number and search order as integers, and amount budgeted as a float.

        Returns:
            str: The string representation of the BudgetCategory object's attributes, labeled.
        """
        return f"General Classification: {self.general_classification}\nBudget Category: {self.budget_category}\nKeywords: {self.keywords}\nOption Number: {self.option_num}\nAmount Budgeted: {self.amt_budgeted}\nSearch Order: {self.search_order}"

    @property
    def keywords(self):
        """
        Getter method for the keywords attribute.

        Returns:
            list: The list of keywords associated with the budget category.
        """
        return self._keywords

    @keywords.setter
    def keywords(self, keywords: str):
        """
        Setter method for the keywords attribute. Transforms a string of keywords separated by '|' into a list of keywords stored in memory.

        Args:
            keywords (str): The keywords to set for the budget category. Expects a list of keywords separated by '|'.

        Raises:
            ValueError: If the provided keywords are not a string.
        """
        if not isinstance(keywords, str):
            raise ValueError("Keywords must be entered as a string.")
        self._keywords = keywords.split('|')

    @property
    def option_num(self):
        """
        Getter method for the option_num attribute.

        Returns:
            int: The option number of the budget category.
        """
        return self._option_num

    @option_num.setter
    def option_num(self, option_num: str):
        """
        Setter method for the option_num attribute. Transforms a numerical string into an integer and ensures input is non-negative.

        Args:
            option_num (str): The option number to set for the budget category.

        Raises:
            ValueError: If the provided option number is negative or cannot be cast to an integer.
        """
        try:
            option_num = int(option_num)
            if option_num < 0:
                raise ValueError
        except ValueError:
            raise ValueError('Option number must be a positive integer')
        self._option_num = option_num

    @property
    def amt_budgeted(self):
        """
        Getter method for the amt_budgeted attribute.

        Returns:
            float: The amount budgeted for the category.
        """
        return self._amt_budgeted

    @amt_budgeted.setter
    def amt_budgeted(self, amt_budgeted: str):
        """
        Setter method for the amt_budgeted attribute. Transforms a string to a float and ensures the input is non-negative.

        Args:
            amt_budgeted (str): The amount budgeted to set for the category.

        Raises:
            ValueError: If the provided amount is negative or cannot be cast to a float.
        """
        try:
            amt_budgeted = round(float(amt_budgeted), 2)
            if amt_budgeted < 0:
                raise ValueError
        except ValueError:
            raise ValueError(
                'Must be a non-negative dollar amount without a currency symbol (ex: 25.75, not $25.75)')
        self._amt_budgeted = amt_budgeted

    @property
    def search_order(self):
        """
        Getter method for the search_order attribute.

        Returns:
            int: The search order of the budget category.
        """
        return self._search_order

    @search_order.setter
    def search_order(self, search_order: str):
        """
        Setter method for the search_order attribute. Transforms a numerical string into an integer and ensures input is non-negative.

        Args:
            search_order (str): The search order to set for the budget category.

        Raises:
            ValueError: If the provided search order is negative or cannot be cast to an integer.
        """
        try:
            search_order = int(search_order)
            if search_order < 0:
                raise ValueError
        except ValueError:
            raise ValueError('Search order must be a positive integer')
        self._search_order = search_order