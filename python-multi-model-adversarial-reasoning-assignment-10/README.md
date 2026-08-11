# Multi-Model Adversarial Reasoning System Assignment 10

## Assignment Summary

This assignment builds a Multi-Model Adversarial Reasoning System using two different company-hosted LLM APIs: Model A and Model B.

The system accepts a text-only scenario or problem statement from the user, such as:

- Business proposal
- Ethical dilemma
- Technical design
- Policy decision

It then orchestrates a structured adversarial reasoning workflow:

```text
Model A -> Model B -> Model A -> Final Evaluation
```

## Required Interaction Flow

1. Model A receives the original input and generates an initial proposal or position with reasoning.
2. Model B receives the original input and Model A's response, then stress-tests it by identifying weaknesses, risks, edge cases, and counterarguments.
3. Model A receives the original input, its first proposal, and Model B's critique, then revises or defends the proposal.
4. A final evaluation summarizes robustness and remaining risks.

Every prompt includes the original user input and the previous model response as context.

## Required Final JSON Format

Successful output is printed as strictly valid JSON:

```json
{
  "original_input": "text-only scenario or problem statement",
  "model_a_initial_proposal": "Model A's initial proposal with reasoning",
  "model_b_critique": "Model B's critique, risks, edge cases, and counterarguments",
  "model_a_revised_response": "Model A's revised or defended proposal",
  "final_evaluation": "concise final evaluation of robustness and remaining risks"
}
```

If the system fails, it still prints valid JSON:

```json
{
  "status": "failed",
  "error": "error message"
}
```

## What This Project Includes

- Separate retry-enabled API client in `llm_client.py`
- Prompt construction logic in `prompt_builder.py`
- Interaction orchestration in `orchestrator.py`
- Response parsing and validation in `validators.py`
- JSON formatting helpers in `json_formatter.py`
- JSONL logging of all prompts, raw responses, and errors
- Local config loading without committing credentials
- Mock model support for testing without real API calls
- Unit tests

## Project Structure

```text
python-multi-model-adversarial-reasoning-assignment-10/
├── README.md
├── requirements.txt
├── .gitignore
├── model_config_example.txt
├── sample_scenario.txt
├── config_loader.py
├── llm_client.py
├── prompt_builder.py
├── logger_utils.py
├── validators.py
├── json_formatter.py
├── mock_models.py
├── orchestrator.py
├── main.py
└── test_adversarial_system.py
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

This validates the workflow without calling real company APIs:

```powershell
python main.py "AI assistant for customer support" --mock
```

You can also run using the included sample file:

```powershell
python main.py --file sample_scenario.txt --mock
```

Expected result: valid JSON with the required final fields.

## Run Tests

```powershell
python test_adversarial_system.py
```

If `python` does not work:

```powershell
py test_adversarial_system.py
```

Expected result:

```text
OK
```

## Configure Real Company Model APIs

Copy the example config locally:

```powershell
Copy-Item .\model_config_example.txt .\local_model_config.txt
notepad .\local_model_config.txt
```

Fill in real Model A and Model B values in `local_model_config.txt`.

Do not commit `local_model_config.txt`. It is ignored by `.gitignore`.

Example format:

```text
MODEL_A_BASE_URL=https://your-company-model-a-server/v1
MODEL_A_MODEL=your-model-a-name
MODEL_A_VERIFY_SSL=false
MODEL_A_USERNAME=your-model-a-username
MODEL_A_PASSWORD=your-model-a-password
MODEL_A_TIMEOUT=300
MODEL_A_RETRIES=2
MODEL_A_RETRY_DELAY=2

MODEL_B_BASE_URL=https://your-company-model-b-server/v1
MODEL_B_MODEL=your-model-b-name
MODEL_B_VERIFY_SSL=false
MODEL_B_USERNAME=your-model-b-username
MODEL_B_PASSWORD=your-model-b-password
MODEL_B_TIMEOUT=300
MODEL_B_RETRIES=2
MODEL_B_RETRY_DELAY=2
```

## Run with Real APIs

```powershell
python main.py "AI assistant for customer support"
```

Or:

```powershell
python main.py --file sample_scenario.txt
```

## Logging

All prompts, raw model outputs, and errors are logged in JSONL format:

```text
logs/adversarial_log.jsonl
```

The log helps prove that the system sent the original input and previous model response as context in each turn.

## Security Notes

- Do not commit passwords, API keys, or private server details.
- Keep real credentials only in `local_model_config.txt`.
- If a credential is exposed, ask the API owner or trainer to rotate it.
