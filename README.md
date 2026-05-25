# Local LLM Vision API Client

A Python script that sends an image to a local vision model (via LM Studio) and gets back structured data about what's in it — using function calling so the response is parseable JSON instead of raw text.

## What it does

You give it an image and a prompt, and it asks the model to identify characters and which movies/shows they're from. Instead of getting a blob of text back, the model calls structured functions (`add_character`, `add_analysis_summary`) so you get clean, usable data.

If the model doesn't support function calling (llava-1.5-7b has limited support), it falls back to plain text automatically.

## Requirements

- Python 3.8+
- [LM Studio](https://lmstudio.ai/) installed, with the `llava-1.5-7b` model loaded and the local server running on `localhost:1234`

To start the server in LM Studio: open the app → go to the "Local Server" tab → click "Start Server".

## Installation

```bash
git clone <repo_url>
cd tp-llm-teddy
pip install -r requirements.txt
```

## Usage

```bash
python main.py --image <path_to_image> --prompt <prompt_text_or_file.txt>
```

Save the text response to a file:
```bash
python main.py --image test-image.png --prompt prompt.txt --output response.txt
```

Save the structured result as JSON (only populated when function calling works):
```bash
python main.py --image test-image.png --prompt prompt.txt --json-output result.json
```

Both flags can be combined:
```bash
python main.py --image test-image.png --prompt prompt.txt --output response.txt --json-output result.json
```

## Files

- `main.py` — the main script
- `prompt.txt` — default prompt asking the model to identify characters and their movies/shows
- `test-image.png` — a sample image to test with
- `requirements.txt` — dependencies (just `requests`)
