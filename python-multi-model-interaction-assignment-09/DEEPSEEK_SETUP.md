# DeepSeek Setup for Multi-Model Interaction Assignment

Your instructor asked you to use the DeepSeek model. The assignment code already supports this because the model name is configurable in `local_model_config.txt`.

Do not commit real usernames, passwords, API keys, or private URLs to GitHub.

## Important

Ask your instructor or API owner for the exact DeepSeek model name available on the company server.

Common examples may look like:

```text
deepseek-r1:8b
deepseek-r1:14b
deepseek-coder
```

Use the exact model name provided by the company server or trainer.

## Option 1: Use DeepSeek as Model A and Llama as Model B

This is useful when the assignment requires two different model APIs or two different model roles.

Create a local config file:

```powershell
Copy-Item .\model_config_example.txt .\local_model_config.txt
notepad .\local_model_config.txt
```

Example format:

```text
MODEL_A_BASE_URL=https://your-company-model-server/v1
MODEL_A_MODEL=deepseek-r1:8b
MODEL_A_VERIFY_SSL=false
MODEL_A_USERNAME=your-username
MODEL_A_PASSWORD=your-password
MODEL_A_TIMEOUT=300

MODEL_B_BASE_URL=https://your-company-model-server/v1
MODEL_B_MODEL=llama3.1:8b
MODEL_B_VERIFY_SSL=false
MODEL_B_USERNAME=your-username
MODEL_B_PASSWORD=your-password
MODEL_B_TIMEOUT=300
```

## Option 2: Use DeepSeek for Both Model A and Model B

Use this only if your instructor says both models can be DeepSeek variants.

Example:

```text
MODEL_A_MODEL=deepseek-r1:8b
MODEL_B_MODEL=deepseek-r1:14b
```

The two models should still be configured as separate Model A and Model B clients in `local_model_config.txt`.

## Run with DeepSeek Config

After saving `local_model_config.txt`, run:

```powershell
python main.py "AI in education"
```

If `python` does not work:

```powershell
py main.py "AI in education"
```

## Run Mock Test First

Before using the real API, verify the project works locally:

```powershell
python main.py "AI in education" --mock
python test_multi_model_system.py
```

Expected test result:

```text
OK
```

## Notes

- `local_model_config.txt` is ignored by `.gitignore`.
- Logs are saved to `logs/interaction_log.jsonl`.
- The final successful output is strict JSON.
- If the DeepSeek server is slow, increase `MODEL_A_TIMEOUT` or `MODEL_B_TIMEOUT` to `300`.
