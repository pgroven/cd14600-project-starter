import unittest
from unittest.mock import call, patch

from balance.balance import Balance
from main import main


class TestMain(unittest.TestCase):
    def setUp(self):
        self.balance = Balance.get_instance()
        self.balance.reset()
        self.addCleanup(self.balance.reset)

    def test_sample_transactions_and_observers(self):
        expected = [
            call("Adding transactions..."),
            call("Transaction($100, category='TransactionCategory.INCOME')"
                 " | Balance: $100.00"),
            call("Transaction($50, category='TransactionCategory.EXPENSE')"
                 " | Balance: $50.00"),
            call("Low balance alert: $50.00"),
            call("Transaction($200, category='TransactionCategory.INCOME')"
                 " | Balance: $250.00"),
            call("Transaction($75, category='TransactionCategory.EXPENSE')"
                 " | Balance: $175.00"),
            call("Transaction($1200, category='TransactionCategory.INCOME')"
                 " | Balance: $1375.00"),
        ]

        with patch("builtins.print") as print_mock:
            main()
            self.assertEqual(print_mock.call_args_list, expected)
            self.assertEqual(self.balance.get_balance(), 1375)

            self.balance.reset()
            print_mock.reset_mock()
            main()
            self.assertEqual(print_mock.call_args_list, expected)

    def test_observers_are_unregistered_after_processing_error(self):
        with patch("builtins.print") as print_mock:
            with patch(
                "main.TransactionCommand.execute", side_effect=ValueError
            ):
                with self.assertRaises(ValueError):
                    main()

            print_mock.reset_mock()
            self.balance.add_income(1)
            print_mock.assert_not_called()


if __name__ == "__main__":
    unittest.main()
