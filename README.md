# Local LLM Vision API Client

## Project Description

This project demonstrates how to interact with a local LLM (Large Language Model) that supports vision capabilities. It sends an image and a text prompt to LM Studio via its API and retrieves the model's response.

## LLM Model Used

**llava-1.5-7b** - A multimodal model capable of understanding and analyzing images.

## Requirements

- Python 3.8+
- LM Studio installed and running on localhost:1234
- llava-1.5-7b model loaded in LM Studio

## Installation

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`

## Usage

```bash
python main.py --image <path_to_image> --prompt <prompt_text_or_file.txt> [--output output.txt]
```

**Example:**

```bash
python main.py --image test-image.png --prompt prompt.txt --output response.txt
```

## Files

- `main.py`
- `prompt.txt`
- `test-image.png`
- `requirements.txt`
