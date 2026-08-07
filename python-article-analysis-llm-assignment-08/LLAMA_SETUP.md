# Llama API Setup for Article Analysis Assignment

This assignment can run with the company-hosted Llama API using environment variables.

Do not save real credentials in GitHub files. Set them only in your local PowerShell session.

## Required Environment Variables

Use the values provided by your company or training team:

```powershell
$env:LLM_PROVIDER="llama"
$env:LLAMA_BASE_URL="https://your-llama-server/v1"
$env:LLAMA_MODEL="llama3.1:8b"
$env:LLAMA_VERIFY_SSL="false"
$env:LLAMA_USERNAME="your-username"
$env:LLAMA_PASSWORD="your-password"
```

`LLAMA_PIN_IP` is normally an access-control or allow-listing value. It is not used directly by the Python code. If the API call fails due to network access, confirm that your system or VPN IP is allowed by the Llama server team.

## How the URL Is Used

If `LLAMA_BASE_URL` is:

```text
https://your-llama-server/v1
```

The script automatically calls:

```text
https://your-llama-server/v1/chat/completions
```

## Run the Llama Version

From the assignment folder:

```powershell
python main_llama.py sample_article.txt
```

If `python` does not work:

```powershell
py main_llama.py sample_article.txt
```

The program prints valid JSON and saves the output to:

```text
llama_analysis_output.json
```

## Run Tests

```powershell
python test_llama_setup.py
python test_article_analyzer.py
```

If `python` does not work:

```powershell
py test_llama_setup.py
py test_article_analyzer.py
```

## Important Security Notes

- Do not commit real passwords or API keys.
- Do not paste credentials into README files.
- If a credential is exposed, ask the API owner or trainer to rotate it.
- Use environment variables each time you open a new PowerShell session.
