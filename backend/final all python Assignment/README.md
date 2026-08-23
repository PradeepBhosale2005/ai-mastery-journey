# Final All Python Assignment

This folder is the final collector location for the Python assignments listed in `backend/Python all assignment .txt`.

Run the packager script to copy the completed numbered assignment folders here and create a ZIP:

```powershell
cd C:\Users\pradeep.bhosale_jade\ai-mastery-journey
git pull
powershell -ExecutionPolicy Bypass -File .\backend\create_final_all_python_assignment.ps1
```

The generated folder will include:

| Assignment | Source Folder | Final Folder |
|---|---|---|
| 01 | `hello-world-python` | `Assignment 01 - Hello World Python` |
| 02 | `python-dsa-problems` | `Assignment 02 - Python DSA Problems` |
| 03 | `python-oop-assignment` | `Assignment 03 - Python OOP Concepts` |
| 04 | `python-numpy-assignment-04` | `Assignment 04 - NumPy Assignment` |
| 05 | `python-pandas-assignment-05` | `Assignment 05 - Pandas Assignment` |

Note: The source file repeats the NumPy assignment content under Assignment 5. The completed numbered Assignment 05 folder in this repository is `python-pandas-assignment-05`, so the packager includes that as Assignment 05.

The ZIP will be created here:

```text
C:\Users\pradeep.bhosale_jade\ai-mastery-journey\backend\final all python Assignment.zip
```
