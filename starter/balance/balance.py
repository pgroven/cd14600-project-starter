# balance.py

from threading import Lock

from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory


class Balance:
    """Singleton to track the balance."""

    _instance = None
    _instance_lock = Lock()

    def __init__(self):
        """Initialize the shared balance once."""
        with self._instance_lock:
            if not hasattr(self, "_balance"):
                self._balance = 0.0
                self._observers = []

    def __new__(cls):
        """Return the one shared Balance instance."""
        with cls._instance_lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
            return cls._instance

    @classmethod
    def get_instance(cls):
        """Get the shared Balance instance."""
        return cls()

    def reset(self):
        """Reset the net balance to zero."""
        self._balance = 0.0

    def add_income(self, amount):
        """Add income to the balance."""
        self.apply_transaction(Transaction(amount, TransactionCategory.INCOME))

    def add_expense(self, amount):
        """Subtract expense from the balance."""
        self.apply_transaction(Transaction(amount, TransactionCategory.EXPENSE))

    def register_observer(self, observer):
        """Register an observer for balance changes."""
        if observer not in self._observers:
            self._observers.append(observer)

    def unregister_observer(self, observer):
        """Unregister an observer from balance changes."""
        if observer in self._observers:
            self._observers.remove(observer)

    def apply_transaction(self, transaction):
        """
        Apply a Transaction object to update the balance.

        Args:
            transaction (Transaction): The transaction to apply.
        """
        if transaction.category == TransactionCategory.INCOME:
            self._balance += transaction.amount
        elif transaction.category == TransactionCategory.EXPENSE:
            self._balance -= transaction.amount
        else:
            raise ValueError(f"Unsupported transaction category: {transaction.category}")
        for observer in tuple(self._observers):
            observer.update(self._balance, transaction)

    def get_balance(self):
        """Get the current net balance."""
        return self._balance

    def summary(self):
        """Return a summary string of the net balance."""
        return f"Current balance: {self._balance:.2f}"
