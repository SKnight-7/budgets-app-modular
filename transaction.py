from datetime import datetime

class Transaction:
    def __init__(self, transaction_num: str, transaction_date: str, amount: float, description: str, category: str = 'Uncategorized', source_file: str = 'sample.csv'):
        self.source_file = source_file
        self.transaction_num = transaction_num
        self.transaction_date = transaction_date
        self.amount = amount
        self.description = description
        self.category = category

    def __str__(self):
        return f"Source: {self.source_file}\nTransaction Number: {self.transaction_num}\nDate: {self.transaction_date}\nAmount: {self.amount}\nDescription: {self.description}\nCategory: {self.category}"

    @property
    def source_file(self):
        return self._source_file

    @source_file.setter
    def source_file(self, source_file: str):
        if not source_file.endswith('.csv'):
            raise ValueError(f'Source files must be of type CSV')
        self._source_file = source_file

    @property
    def transaction_num(self):
        return self._transaction_num

    @transaction_num.setter
    def transaction_num(self, transaction_num: str):
        try:
            transaction_num = int(transaction_num)
            if transaction_num < 0:
                raise ValueError('Transaction number must be non-negative')
        except ValueError:
            raise ValueError('Transaction number must be an integer')
        self._transaction_num = transaction_num

    @property
    def transaction_date(self):
        return self._transaction_date

    @transaction_date.setter
    def transaction_date(self, transaction_date: str):
        try:
            transaction_date = datetime.strptime(transaction_date, '%Y-%m-%d')
        except ValueError:
            raise ValueError('Must be a valid date')
        self._transaction_date = transaction_date

    @property
    def amount(self):
        """
        Getter method for the amount attribute.

        Returns:
            float: The amount of the transaction.
        """
        return self._amount

    @amount.setter
    def amount(self, amount: str):
        """
        Setter method for the amount attribute. Transforms a string to a float and ensures the input is non-negative.

        Args:
            amount (str): The amount to set for the transaction.

        Raises:
            ValueError: If the provided amount is negative or cannot be cast to a float.
        """
        try:
            amount = round(float(amount), 2)
        except ValueError:
            raise ValueError(
                'Must be a dollar amount without a currency symbol (ex: 25.75, not $25.75)')
        self._amount = amount