"""Command for applying a transaction to a balance."""


class TransactionCommand:
    """Encapsulate a transaction and its balance operation."""

    def __init__(self, balance, transaction):
        self.balance = balance
        self.transaction = transaction

    def execute(self):
        """Apply the transaction through the balance's notification path."""
        self.balance.apply_transaction(self.transaction)
