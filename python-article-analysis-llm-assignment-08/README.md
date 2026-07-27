# Article Analysis System Assignment 08

## Assignment Summary

This assignment builds an Article Analysis System using a company-hosted LLM API.

The application accepts an article as input, constructs a well-designed prompt, sends the article to the configured LLM API, and validates the response programmatically.

The LLM response must be strictly valid JSON and must contain these fields:

```json
{
  "summary": "summary within 150 words",
  "important_points": ["point 1", "point 2", "point 3", "point 4", "point 5"],
  "key_themes": ["theme 1", "theme 2", "theme 3"],
  "target_audience": "brief audience description"
}
```

## Required Output Fields

### summary

A concise article summary limited to 150 words.

### important_points

An array of 5 to 10 clearly written strings that capture the core ideas of the article.

### key_themes

An array of 3 to 5 short phrases, not full sentences.

### target_audience

A brief identification of the most relevant audience for the article.

## What This Project Includes

- Strict JSON-only prompt construction
- Company LLM API request handling
- Support for OpenAI-style response format
- JSON parsing and validation
- Summary word-count validation
- important_points count validation
- key_themes count validation
- Graceful error handling for API failures
- Graceful error handling for malformed LLM responses
- Unit tests that run without calling the real API

## Project Structure

```text
python-article-analysis-llm-assignment-08/
├── README.md
├── requirements.txt
├── article_analyzer.py
├── main.py
├── sample_article.txt
├── mock_valid_response.json
└── test_article_analyzer.py
```

## Requirements

- Python installed on the system
- Visual Studio Code or any code editor
- Company-hosted LLM API URL
- Company-hosted LLM API key, if required

Install Python dependencies:

```bash
python -m pip install -r requirements.txt
```

If `python` does not work, try:

```bash
py -m pip install -r requirements.txt
```

## API Configuration

Set these environment variables before running the real API call:

```powershell
$env:COMPANY_LLM_API_URL="https://your-company-llm-api-endpoint"
$env:COMPANY_LLM_API_KEY="your-api-key"
$env:COMPANY_LLM_MODEL="your-model-name"
```

`COMPANY_LLM_MODEL` is optional. Use it only if the company API requires a model name.

Important: Do not commit real API keys to GitHub.

## How to Run After Extracting ZIP File

### Step 1: Extract the ZIP File

Extract the submitted ZIP file on your system.

### Step 2: Open the Folder

Open the extracted folder in Visual Studio Code or any code editor.

### Step 3: Open Terminal

Open PowerShell, Command Prompt, or the integrated terminal in Visual Studio Code.

### Step 4: Go to the Assignment Folder

```bash
cd python-article-analysis-llm-assignment-08
```

### Step 5: Install Requirements

```bash
python -m pip install -r requirements.txt
```

### Step 6: Run Local Mock Validation

This validates the parsing and JSON schema without calling the real company API:

```bash
python main.py sample_article.txt --mock-response mock_valid_response.json
```

Expected result: formatted JSON output with summary, important_points, key_themes, and target_audience.

### Step 7: Run with Company LLM API

Set the environment variables first:

```powershell
$env:COMPANY_LLM_API_URL="https://your-company-llm-api-endpoint"
$env:COMPANY_LLM_API_KEY="your-api-key"
```

Then run:

```bash
python main.py sample_article.txt
```

The program will:

1. Read the article from `sample_article.txt`
2. Build the JSON-only LLM prompt
3. Send the prompt to the company-hosted LLM API
4. Parse the LLM response
5. Validate the response structure and constraints
6. Print valid JSON output

### Step 8: Run Tests

```bash
python test_article_analyzer.py
```

If `python` does not work, try:

```bash
py test_article_analyzer.py
```

Expected test result:

```text
OK
```

## Notes About Company API Format

The implementation uses a generic OpenAI-compatible chat payload:

```json
{
  "messages": [
    {"role": "system", "content": "..."},
    {"role": "user", "content": "..."}
  ],
  "temperature": 0.2,
  "response_format": {"type": "json_object"}
}
```

If the company-hosted LLM API expects a different request body, update only this function in `article_analyzer.py`:

```python
build_api_payload()
```

The response parser already supports common response formats such as:

- Direct JSON object with required fields
- `choices[0].message.content`
- `choices[0].text`
- `output_text`
- `content`
- `response`

## Error Handling

The application handles:

- Missing API URL
- API connection failure
- Non-JSON API response
- Malformed LLM JSON output
- Missing required fields
- Extra unexpected fields
- More than 150 words in summary
- Fewer than 5 or more than 10 important points
- Fewer than 3 or more than 5 key themes
- Empty target audience

## Assignment Status

Completed for the Article Analysis System assignment in NEURALIS Phase 2.1.
