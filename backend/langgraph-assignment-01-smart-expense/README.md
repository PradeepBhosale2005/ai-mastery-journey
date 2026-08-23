# LangGraph Assignment 01: Smart Expense Processing Workflow

This folder contains a complete LangGraph solution for the Smart Expense Processing assignment from `backend/AssignmentPrompt.txt`.

## Assignment Requirement

Build a LangGraph workflow that processes a user's expense and decides how it should be handled based on the amount.

The workflow must:

1. Accept an expense amount in USD.
2. Add 10% tax to the expense.
3. Convert the final taxed amount to INR.
4. Route based on the original submitted USD amount:
   - `amount <= 100 USD` -> `Auto Approved`
   - `100 < amount <= 1000 USD` -> `Manager Approval`
   - `amount > 1000 USD` -> `Finance Department Approval`
5. Print the final decision and converted amount.

## Project Files

```text
backend/langgraph-assignment-01-smart-expense/
├── README.md
├── requirements.txt
├── .gitignore
├── expense_workflow.py
├── main.py
├── run_examples.py
└── test_expense_workflow.py
```

## Graph Design

```text
START
  |
  v
add_tax
  |
  v
convert_to_inr
  |
  v
conditional route by original USD amount
  |-------------|----------------|----------------|
  v             v                v
Auto Approved   Manager Approval Finance Department Approval
  |             |                |
  v             v                v
END           END              END
```

## Setup

From the repository root:

```powershell
cd C:\Users\pradeep.bhosale_jade\ai-mastery-journey
git pull
cd .\backend\langgraph-assignment-01-smart-expense
python -m pip install -r requirements.txt
```

## Run the Workflow

Run with the default amount, `250 USD`:

```powershell
python main.py
```

Run with a custom amount:

```powershell
python main.py 50
python main.py 500
python main.py 1500
```

Run with a custom USD to INR rate:

```powershell
python main.py 500 --rate 83
```

## Run All Example Routes

```powershell
python run_examples.py
```

This demonstrates:

```text
50 USD   -> Auto Approved
500 USD  -> Manager Approval
1500 USD -> Finance Department Approval
```

## Run Tests

```powershell
python test_expense_workflow.py
```

The tests validate:

- the graph compiles
- 10% tax calculation
- USD to INR conversion
- Auto Approved route
- Manager Approval route
- Finance Department Approval route
- boundary conditions at 100 and 1000 USD
- negative amount validation

## Safe ZIP for LMS Upload

Create a safe ZIP from the repository root:

```powershell
cd C:\Users\pradeep.bhosale_jade\ai-mastery-journey

$src = ".\backend\langgraph-assignment-01-smart-expense"
$tmp = ".\backend\langgraph-assignment-01-smart-expense-submit"
$zip = ".\backend\langgraph-assignment-01-smart-expense.zip"

Remove-Item $tmp -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item $zip -Force -ErrorAction SilentlyContinue
Copy-Item $src $tmp -Recurse

Remove-Item "$tmp\.env" -Force -ErrorAction SilentlyContinue
Remove-Item "$tmp\.venv" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item "$tmp\venv" -Recurse -Force -ErrorAction SilentlyContinue
Get-ChildItem $tmp -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force
Get-ChildItem $tmp -Recurse -File -Filter "*.pyc" | Remove-Item -Force

Compress-Archive -Path $tmp -DestinationPath $zip -Force
Remove-Item $tmp -Recurse -Force
```

Upload:

```text
C:\Users\pradeep.bhosale_jade\ai-mastery-journey\backend\langgraph-assignment-01-smart-expense.zip
```
