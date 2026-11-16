import unittest
from unittest.mock import Mock, call, patch
from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory
from balance.balance import Balance
from balance.balance_observer import LowBalanceAlertObserver, PrintObserver

class TestLowBalanceAlertObserver(unittest.TestCase):

    def setUp(self):
        self.balance = Balance.get_instance()
        self.balance.reset()

    def test_alert_triggers_on_low_balance(self):
        observer = LowBalanceAlertObserver(threshold=50)
        self.balance.register_observer(observer)
        self.addCleanup(self.balance.unregister_observer, observer)

        self.balance.apply_transaction(Transaction(100, TransactionCategory.INCOME))
        self.assertFalse(observer.alert_triggered)

        self.balance.apply_transaction(Transaction(60, TransactionCategory.EXPENSE))
        self.assertTrue(observer.alert_triggered)

        self.balance.apply_transaction(Transaction(100, TransactionCategory.INCOME))
        self.assertFalse(observer.alert_triggered)

        self.balance.apply_transaction(Transaction(60, TransactionCategory.EXPENSE))
        self.assertFalse(observer.alert_triggered)
        
        self.balance.apply_transaction(Transaction(60, TransactionCategory.EXPENSE))
        self.assertTrue(observer.alert_triggered)

    def test_direct_expense_updates_observer(self):
        observer = LowBalanceAlertObserver(threshold=50)
        self.balance.register_observer(observer)
        self.addCleanup(self.balance.unregister_observer, observer)

        self.balance.add_expense(60)

        self.assertTrue(observer.alert_triggered)

    def test_alert_is_cleared_at_threshold(self):
        observer = LowBalanceAlertObserver(threshold=50)
        self.balance.register_observer(observer)
        self.addCleanup(self.balance.unregister_observer, observer)

        self.balance.add_income(49)
        self.assertTrue(observer.alert_triggered)
        self.balance.add_income(1)
        self.assertFalse(observer.alert_triggered)

    def test_observers_receive_updates_once_and_can_unregister(self):
        observer = Mock()
        other_observer = Mock()
        self.balance.register_observer(observer)
        self.balance.register_observer(observer)
        self.balance.register_observer(other_observer)
        self.addCleanup(self.balance.unregister_observer, observer)
        self.addCleanup(self.balance.unregister_observer, other_observer)

        transaction = Transaction(100, TransactionCategory.INCOME)
        self.balance.apply_transaction(transaction)
        observer.update.assert_called_once_with(100, transaction)
        self.assertIs(observer.update.call_args.args[1], transaction)
        other_observer.update.assert_called_once_with(100, transaction)

        self.balance.unregister_observer(observer)
        self.balance.add_expense(20)
        observer.update.assert_called_once()
        self.assertEqual(
            other_observer.update.call_args_list,
            [call(100, transaction), call(80, Transaction(20, TransactionCategory.EXPENSE))],
        )

    def test_invalid_transaction_does_not_notify_observer(self):
        observer = Mock()
        self.balance.register_observer(observer)
        self.addCleanup(self.balance.unregister_observer, observer)

        with self.assertRaises(ValueError):
            self.balance.apply_transaction(Transaction(10, "invalid"))
        observer.update.assert_not_called()
        self.assertEqual(self.balance.get_balance(), 0)

    def test_print_observer_reports_transaction_and_balance(self):
        observer = PrintObserver()
        self.balance.register_observer(observer)
        self.addCleanup(self.balance.unregister_observer, observer)

        with patch("builtins.print") as print_mock:
            self.balance.add_income(12.5)

        print_mock.assert_called_once_with(
            "Transaction($12.5, category='TransactionCategory.INCOME') | Balance: $12.50"
        )

if __name__ == "__main__":
    unittest.main()
