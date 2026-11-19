import unittest
from unittest.mock import Mock

from balance.balance import Balance
from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory
from transaction.transaction_command import TransactionCommand


class TestTransactionCommand(unittest.TestCase):
    def setUp(self):
        self.balance = Balance.get_instance()
        self.balance.reset()
        self.addCleanup(self.balance.reset)

    def test_income_is_applied_once_on_execution(self):
        command = TransactionCommand(
            self.balance, Transaction(25, TransactionCategory.INCOME)
        )

        self.assertEqual(self.balance.get_balance(), 0.0)
        command.execute()
        self.assertEqual(self.balance.get_balance(), 25.0)

    def test_execute_applies_transaction_and_notifies_observer(self):
        observer = Mock()
        self.balance.register_observer(observer)
        self.addCleanup(self.balance.unregister_observer, observer)
        transaction = Transaction(30, TransactionCategory.EXPENSE)
        command = TransactionCommand(self.balance, transaction)

        self.assertEqual(self.balance.get_balance(), 0)
        command.execute()

        self.assertEqual(self.balance.get_balance(), -30)
        observer.update.assert_called_once_with(-30, transaction)

    def test_execute_propagates_invalid_category(self):
        command = TransactionCommand(self.balance, Transaction(10, "invalid"))

        with self.assertRaises(ValueError):
            command.execute()
        self.assertEqual(self.balance.get_balance(), 0)


if __name__ == "__main__":
    unittest.main()
