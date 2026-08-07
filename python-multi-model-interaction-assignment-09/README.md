# Multi-Model Interaction System Assignment 09

## Assignment Summary

This assignment builds a Multi-Model Interaction System using two different company-hosted LLM APIs: Model A and Model B.

The application accepts a topic from the user and orchestrates a structured discussion:

```text
Model A -> Model B -> Model A -> Synthesis
```

The interaction includes at least three structured turns:

1. Model A gives an initial position, explanation, or argument on the topic.
2. Model B critiques, questions, or expands upon Model A's response.
3. Model A gives a final reply using Model B's critique as context.
4. Model B is used again to generate a short synthesized conclusion.

The final output is printed as strictly valid JSON.

## Required Final JSON Format

```json
{
  "topic": "original topic",
  "model_a_initial_response": "Model A initial response",
  "model_b_critique_response": "Model B critique or counter-response",
  "model_a_final_reply": "Model A final reply",
  "synthesized_conclusion": "short synthesized conclusion"
}
```

No extra text is printed outside the JSON object when the command succeeds.

If the application fails, it still prints valid JSON:

```json
{
  "status": "failed",
  "error": "error message"
}
```

## What This Project Includes

- Separate reusable API client for company-hosted LLM APIs
- Prompt construction logic separated into `prompts.py`
- Interaction orchestration separated into `orchestrator.py`
- JSON parsing and validation separated into `validators.py`
- JSONL logging of all prompts and raw model outputs
- Mock mode for testing without real API calls
- Local config loading without committing credentials
- Unit tests

## Project Structure

```text
python-multi-model-interaction-assignment-09/
├── README.md
├── requirements.txt
├── .gitignore
├── model_config_example.txt
├── config_loader.py
├── llm_client.py
├── logger_utils.py
├── mock_models.py
├── orchestrator.py
├── prompts.py
├── validators.py
├── main.py
└── test_multi_model_system.py
```

## Install Requirements

```powershell
python -m pip install -r requirements.txt
```

If `python` does not work:

```powershell
py -m pip install -r requirements.txt
```

## Run with Mock Models First

This does not call the real company APIs:

```powershell
python main.py "AI in education" --mock
```

If `python` does not work:

```powershell
py main.py "AI in education" --mock
```

This should print valid JSON output and create logs in:

```text
logs/interaction_log.jsonl
```

## Run Tests

```powershell
python test_multi_model_system.py
```

If `python` does not work:

```powershell
py test_multi_model_system.py
```

Expected result:

```text
OK
```

## Configure Real Company Model APIs

Copy the example file locally:

```powershell
Copy-Item .\model_config_example.txt .\local_model_config.txt
notepad .\local_model_config.txt
```

Fill in the real values for Model A and Model B.

Do not commit `local_model_config.txt`. It is ignored by `.gitignore`.

Example local config format:

```text
MODEL_A_BASE_URL=https://model-a-company-server/v1
MODEL_A_MODEL=model-a-name
MODEL_A_VERIFY_SSL=false
MODEL_A_USERNAME=your-model-a-username
MODEL_A_PASSWORD=your-model-a-password
MODEL_A_TIMEOUT=180

MODEL_B_BASE_URL=https://model-b-company-server/v1
MODEL_B_MODEL=model-b-name
MODEL_B_VERIFY_SSL=false
MODEL_B_USERNAME=your-model-b-username
MODEL_B_PASSWORD=your-model-b-password
MODEL_B_TIMEOUT=180
```

## Run with Real Company APIs

After creating `local_model_config.txt`, run:

```powershell
python main.py "AI in education"
```

If `python` does not work:

```powershell
py main.py "AI in education"
```

## Logging

The system logs all prompts and raw model outputs in JSONL format:

```text
logs/interaction_log.jsonl
```

Each log entry includes:

- timestamp
- event_type
- turn
- model_name
- prompt or raw_output

## Validation Rules

The system validates that:

- Each model returns strictly valid JSON.
- Model A and Model B responses use the required `response` field.
- The synthesis response uses the required `conclusion` field.
- Final output contains the required fields only.
- Each response appears relevant to the user-provided topic.
- API failures and validation failures are handled gracefully with valid JSON error output.

## Security Notes

- Do not commit real usernames, passwords, tokens, or API keys.
- Keep real values only in `local_model_config.txt` on your laptop.
- If a credential is exposed, ask the API owner or trainer to rotate it.

## Assignment Status

Completed for the Multi-Model Interaction System assignment in NEURALIS Phase 2.1.
