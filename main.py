import requests
import base64
import argparse
import sys
import json

API_URL = "http://localhost:1234/v1/chat/completions"
MODEL_ID = "llava-1.5-7b"

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "add_character",
            "description": "Add a character identified in the image with their movie or show origin",
            "parameters": {
                "type": "object",
                "properties": {
                    "character_name": {
                        "type": "string",
                        "description": "The name of the character"
                    },
                    "movie_or_show": {
                        "type": "string",
                        "description": "The movie or TV show the character appears in"
                    },
                    "description": {
                        "type": "string",
                        "description": "Brief physical description of the character as seen in the image"
                    },
                    "actor": {
                        "type": "string",
                        "description": "The actor who plays this character (if known)"
                    }
                },
                "required": ["character_name", "movie_or_show", "description"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "add_analysis_summary",
            "description": "Provide a final summary of all characters found in the image",
            "parameters": {
                "type": "object",
                "properties": {
                    "total_characters": {
                        "type": "integer",
                        "description": "Total number of characters identified"
                    },
                    "summary": {
                        "type": "string",
                        "description": "A brief overall summary of the image and its characters"
                    }
                },
                "required": ["total_characters", "summary"]
            }
        }
    }
]


def encode_image(image_path):
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except FileNotFoundError:
        print(f"Error: The file '{image_path}' was not found.")
        sys.exit(1)


def get_prompt(prompt_source):
    if prompt_source.endswith('.txt'):
        try:
            with open(prompt_source, 'r', encoding='utf-8') as file:
                return file.read().strip()
        except FileNotFoundError:
            print(f"Error: The prompt file '{prompt_source}' was not found.")
            sys.exit(1)
    return prompt_source


def send_request(prompt, base64_image):
    payload = {
        "model": MODEL_ID,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "tools": TOOLS,
        "tool_choice": "auto",
        "temperature": 0.2,
        "max_tokens": 800
    }

    headers = {"Content-Type": "application/json"}

    print("Sending request to LM Studio...")
    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error {response.status_code}: {response.text}")
        sys.exit(1)


def process_tool_calls(tool_calls):
    characters = []
    summary = None

    for tool_call in tool_calls:
        function_name = tool_call["function"]["name"]
        arguments = json.loads(tool_call["function"]["arguments"])

        if function_name == "add_character":
            characters.append(arguments)
        elif function_name == "add_analysis_summary":
            summary = arguments

    return characters, summary


def format_results(characters, summary):
    lines = []

    if characters:
        lines.append(f"Characters identified: {len(characters)}\n")
        for i, char in enumerate(characters, 1):
            lines.append(f"Character {i}: {char['character_name']}")
            lines.append(f"  Movie/Show : {char['movie_or_show']}")
            lines.append(f"  Description: {char['description']}")
            if char.get('actor'):
                lines.append(f"  Played by  : {char['actor']}")
            lines.append("")

    if summary:
        lines.append(f"Summary: {summary['summary']}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Local LLM Vision API Client with Function Calling")
    parser.add_argument("--image", required=True, help="Path to the image file")
    parser.add_argument("--prompt", required=True, help="Text prompt OR path to a .txt file")
    parser.add_argument("--output", help="Optional: Path to save the text response", default=None)
    parser.add_argument("--json-output", help="Optional: Path to save structured JSON output", default=None)

    args = parser.parse_args()

    prompt_text = get_prompt(args.prompt)
    print(f"Prompt loaded: '{prompt_text}'")

    base64_image = encode_image(args.image)

    api_response = send_request(prompt_text, base64_image)

    message = api_response['choices'][0]['message']

    if message.get('tool_calls'):
        print("\n=== Function Calling Response ===\n")
        characters, summary = process_tool_calls(message['tool_calls'])
        llm_output = format_results(characters, summary)

        print(llm_output)
        print("\n=================================\n")

        if args.json_output:
            structured_data = {"characters": characters, "summary": summary}
            with open(args.json_output, "w", encoding="utf-8") as f:
                json.dump(structured_data, f, indent=2, ensure_ascii=False)
            print(f"Structured JSON saved to {args.json_output}")
    else:
        # llava-1.5-7b may not support native tool_calls — plain text fallback
        print("\n[Info] Model returned plain text (function calling not supported by this model)\n")
        llm_output = message['content']
        print("\n=== LLM Response ===\n")
        print(llm_output)
        print("\n====================\n")

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(llm_output)
        print(f"Response saved to {args.output}")


if __name__ == "__main__":
    main()
