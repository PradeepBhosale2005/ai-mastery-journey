# Tokenizer Assignment 07

## Assignment Summary

This assignment implements a simple tokenizer in Python.

The tokenizer takes one or more sentences as input and splits the text into individual word tokens. Each unique token is assigned a unique numerical ID.

The tokenizer maintains its own vocabulary internally:

- Stores all unique words it encounters
- Assigns a unique integer ID to each new word
- Reuses the existing ID if a word already exists
- Updates the vocabulary dynamically as new text is processed

## Example

Input:

```text
This is a test. This test is simple.
```

Tokens:

```text
["this", "is", "a", "test", "this", "test", "is", "simple"]
```

Vocabulary:

```python
{"this": 1, "is": 2, "a": 3, "test": 4, "simple": 5}
```

Token IDs:

```text
[1, 2, 3, 4, 1, 4, 2, 5]
```

## Learning Goals

- Understand basic text tokenization
- Convert text to lowercase
- Remove punctuation while keeping words
- Build and maintain a vocabulary dictionary
- Assign unique numerical IDs to words
- Reuse IDs for repeated words
- Dynamically update the vocabulary when new text is processed

## Requirements

- Python installed on the system
- Visual Studio Code or any code editor

No external Python libraries are required.

## Project Structure

```text
python-tokenizer-assignment-07/
├── README.md
├── tokenizer.py
└── test_tokenizer.py
```

## How to Run After Extracting ZIP File

### Step 1: Extract the ZIP File

Extract the submitted ZIP file on your system.

### Step 2: Open the Folder

Open the extracted folder in Visual Studio Code or any code editor.

### Step 3: Open Terminal

Open PowerShell, Command Prompt, or the integrated terminal in Visual Studio Code.

### Step 4: Go to the Assignment Folder

```bash
cd python-tokenizer-assignment-07
```

### Step 5: Run the Tokenizer Program

```bash
python tokenizer.py
```

If `python` does not work, try:

```bash
py tokenizer.py
```

### Step 6: Run Test Cases

```bash
python test_tokenizer.py
```

If `python` does not work, try:

```bash
py test_tokenizer.py
```

Expected test result:

```text
OK
```

## Files Included

### tokenizer.py

Contains the `SimpleTokenizer` class and sample demo.

Main methods:

- `tokenize(text)` - splits text into lowercase tokens
- `encode(text)` - converts text into token IDs and updates vocabulary
- `process_text(text)` - returns tokens, token IDs, and vocabulary
- `process_sentences(sentences)` - handles one sentence or multiple sentences
- `get_vocabulary()` - returns the current vocabulary
- `decode(token_ids)` - converts token IDs back to words

### test_tokenizer.py

Contains unit tests to verify:

- punctuation removal
- lowercase conversion
- vocabulary creation
- repeated word ID reuse
- dynamic vocabulary update
- multiple sentence processing
- ID decoding

## GitHub Repository

Repository: `PradeepBhosale2005/ai-mastery-journey`

Assignment folder: `python-tokenizer-assignment-07`

## Assignment Status

Completed for the Tokenizer assignment in NEURALIS Phase 2.1.
