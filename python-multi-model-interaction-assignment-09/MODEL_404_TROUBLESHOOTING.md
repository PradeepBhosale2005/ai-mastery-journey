# Model API 404 Troubleshooting

## What the Error Means

A message like this means the server was reachable, but the requested API route or model was not found:

```text
404 Client Error: Not Found for url: .../v1/chat/completions
```

This is different from a network failure. It usually means one of these is wrong:

1. The server does not support the OpenAI-compatible `/chat/completions` route.
2. The base URL should be different.
3. The model name is not exactly the name exposed by the company server.
4. The DeepSeek model exists on a different endpoint or deployment.

## First Step

Run the diagnostic script:

```powershell
python diagnose_model_api.py
```

If `python` does not work:

```powershell
py diagnose_model_api.py
```

The script checks common endpoint styles:

- OpenAI-compatible `/models`
- OpenAI-compatible `/chat/completions`
- Ollama-style `/api/tags`
- Ollama-style `/api/chat`

## What to Look For

### If `/models` works

Look at the model list and copy the exact DeepSeek model name into `local_model_config.txt`.

Example:

```text
MODEL_A_MODEL=exact-deepseek-model-name-from-server
```

### If `/models` fails but `/api/tags` works

The server is likely using an Ollama-style API instead of the OpenAI-compatible API.

Ask the instructor/API owner whether the assignment should use the `/api/chat` endpoint.

### If everything returns 404

Ask the instructor/API owner for the exact API endpoint for DeepSeek.

### If the request times out

Increase the timeout:

```text
MODEL_A_TIMEOUT=300
MODEL_B_TIMEOUT=300
```

## Important

Do not paste passwords or full credential files into GitHub, README files, or screenshots.
