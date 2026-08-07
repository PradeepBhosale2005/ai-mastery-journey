# Llama API Timeout Troubleshooting

## What the Error Means

This warning is expected when `LLAMA_VERIFY_SSL=false`:

```text
InsecureRequestWarning: Unverified HTTPS request is being made
```

It is only a warning. The actual failure is:

```text
Read timed out. (read timeout=60)
```

That means the Llama server did not send a complete response within 60 seconds.

## Quick Fix

Use the longer-timeout runner:

```powershell
$env:LLAMA_TIMEOUT="180"
python main_llama_long_timeout.py sample_article.txt
```

If the server is still slow, try:

```powershell
$env:LLAMA_TIMEOUT="300"
python main_llama_long_timeout.py sample_article.txt
```

## Check the Server Before Running the Full Assignment

Run:

```powershell
python check_llama_connection.py
```

This checks:

1. `/models`
2. `/chat/completions` with a very small prompt

If `/models` works but `/chat/completions` times out, the model server may be busy or slow.

If both fail, check VPN, network, credentials, server URL, port, or IP allow-listing.

## Reduce Article Size

If the article is long, test with a shorter article first. Large prompts can take longer to process.

## Network and Access Checks

Confirm these with your trainer/API owner:

- You are connected to the correct VPN or network.
- Your system IP is allowed if IP allow-listing is used.
- The Llama server is running.
- The model name is correct.
- The username and password are valid.

## SSL Warning

Because the provided setup uses:

```powershell
$env:LLAMA_VERIFY_SSL="false"
```

Python will warn that SSL verification is disabled. This is expected for that configuration. If the company provides a valid certificate setup, use:

```powershell
$env:LLAMA_VERIFY_SSL="true"
```
