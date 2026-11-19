# Personal Finance Manager — Design Patterns Project

This project is a hands-on exercise in applying Object-Oriented Design Patterns to build a simplified personal finance manager.
You will implement and extend starter code to add functionality such as tracking transactions, adapting external data, observing balance changes, and ensuring proper architectural patterns.

## Getting Started

### Dependencies

Make sure you have python version >= 3.10.x installed on your computer. 

The optional style check uses `pycodestyle`, listed in `requirements.txt`.
From the repository root, create a virtual environment and install it:

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
```

On macOS or Linux, use `.venv/bin/python` instead of
`.\.venv\Scripts\python`.

### Installation

1. Clone the repo:

```
bash
git clone https://github.com/udacity/cd14600-project-starter.git
cd cd14600-project-starter/starter
```

2. Run the Program: 
```
python main.py
```

## Testing

This project uses Python’s built-in unittest framework.

From the `starter` directory, run all tests:

```
python -m unittest test_main balance.test_balance balance.test_balance_observer transaction.test_transaction transaction.test_transaction_adapter transaction.test_transaction_command
```

To run a single test file:
```
python -m unittest balance/test_balance_observer.py
```

To check PEP 8 style from the repository root:

```powershell
.\.venv\Scripts\python -m pycodestyle starter
```

### Break Down Tests

- test_balance.py → Verifies the Singleton Balance class and transaction balance updates.
- test_transaction.py → Checks transaction creation, formatting, and equality.
- test_transaction_adapter.py → Ensures external income data is correctly adapted into Transaction objects.
- test_balance_observer.py → Validates that low-balance alerts are triggered at the correct threshold.
- test_transaction_command.py → Checks transaction command execution and errors.
- test_main.py → Checks the sample balances and visible warning.

## Design Reflection

**Singleton.** The finance manager needs one running total, so both `Balance()`
and `Balance.get_instance()` return the same balance. This gives transactions
and observers a consistent view, but shared state can leak between tests.
`TestBalance.setUp()` resets the balance to keep each test independent.

**Adapter.** Freelance income has a different representation from the internal
`Transaction`. `TransactionAdapter.to_transaction()` converts its amount to an
income transaction, allowing `Balance` to process it like any other income.
The trade-off is that the conversion assumes freelance entries are income and
does not carry over the invoice ID or description.

**Observer.** Balance changes need both a running display and a low-balance
warning. `Balance` notifies `PrintObserver` and `LowBalanceAlertObserver`
without depending on their output logic; the sample warns below $100, not at
$100. This flexibility requires careful registration and cleanup: `main()`
unregisters its observers, and observer tests use cleanup to prevent callbacks
from leaking into other tests.

**Command.** `TransactionCommand` wraps a transaction and its target balance,
so `main()` can execute each operation through the same validation and
notification path. It separates creating an action from applying it, as tested
by the balance before and after `execute()`. The extra object adds complexity,
and executing it again applies the transaction again; it does not provide undo.

## Project Instructions

1. Implement Singleton Balance Class – Ensure only one balance object exists throughout the app.
2. Complete Transaction Class – Handle income and expense transactions.
3. Implement Adapter Pattern – Adapt external freelance income data into internal Transaction objects.
4. Implement Observer Pattern – Create a low balance observer that triggers an alert when funds drop too low.
5. Add Unit Tests – Write tests for all implemented functionality.
6. Choose and Implement a Fourth Pattern – Pick one additional design pattern (e.g., Strategy, Command, Decorator, etc.) and integrate it into your project.
7. Provide a Reflection – Add a short write-up in your repo (README or separate file) explaining your design choices.

## Built With

* [Python](https://www.python.org/) – Main programming language
* [unittest](https://docs.python.org/3/library/unittest.html) – Testing framework
* [PEP8](https://peps.python.org/pep-0008/) – Style guide for Python code

## License

[License](LICENSE.txt)
