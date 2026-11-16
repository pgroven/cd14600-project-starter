import unittest
from balance.balance import Balance
from transaction.external_income_transaction import ExternalFreelanceIncome
from transaction.transaction_adapter import TransactionAdapter
from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory

class TestTransactionAdapter(unittest.TestCase):

    def test_adapter_converts_freelance_income(self):
        ext_txn = ExternalFreelanceIncome(500, "INV-12345", "Website development")
        adapter = TransactionAdapter(ext_txn)
        txn = adapter.to_transaction()
        self.assertEqual(txn, Transaction(500, TransactionCategory.INCOME))

    def test_adapted_income_updates_balance(self):
        balance = Balance.get_instance()
        balance.reset()
        self.addCleanup(balance.reset)
        adapter = TransactionAdapter(ExternalFreelanceIncome(12.50, "INV-2", "Consulting"))

        balance.apply_transaction(adapter.to_transaction())

        self.assertEqual(balance.get_balance(), 12.50)

if __name__ == "__main__":
    unittest.main()
