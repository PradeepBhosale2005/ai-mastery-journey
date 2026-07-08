# Install Troubleshooting for Pandas Assignment

## Problem

On Windows, installing the full `requirements.txt` may fail while installing Jupyter because some JupyterLab files have very long paths.

Typical error:

```text
OSError: [Errno 2] No such file or directory
HINT: This error might have occurred since this system does not have Windows Long Path support enabled.
```

When this happens, the installation stops before Pandas is available, so running the scripts may show:

```text
ModuleNotFoundError: No module named 'pandas'
```

## Quick Fix for Python Script Assignments

Use the lightweight requirements file first:

```bash
python -m pip install -r requirements-lite.txt
```

This installs only:

```text
pandas
numpy
matplotlib
```

Then run:

```bash
python run_all.py
python test_pandas_assignment.py
```

If `python` does not work, use:

```bash
py -m pip install -r requirements-lite.txt
py run_all.py
py test_pandas_assignment.py
```

## Notebook Option

The Python script assignments do not require Jupyter. Jupyter is only needed for opening `notebooks/iris_analysis.ipynb`.

If Jupyter installation fails because of Windows long path issues, complete and submit the script assignment first. The notebook file is already included in the folder.

## Optional Long Path Fix

If you want to install Jupyter locally, enable Windows Long Path support or raise a JService ticket for Python/Jupyter setup support.
