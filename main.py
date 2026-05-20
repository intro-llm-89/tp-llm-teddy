import requests
import base64
import argparse
import sys

API_URL = "http://localhost:1234/v1/chat/completions"
MODEL_ID = "llava-1.5-7b"

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
        "temperature": 0.2,
        "max_tokens": 400
    }

    headers = {"Content-Type": "application/json"}
    
    print("Sending request to LM Studio...")
    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error {response.status_code}: {response.text}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Local LLM Vision API Client")
    parser.add_argument("--image", required=True, help="Path to the image file")
    parser.add_argument("--prompt", required=True, help="Text prompt OR path to a .txt file")
    parser.add_argument("--output", help="Optional: Path to save the text response", default=None)
    
    args = parser.parse_args()

    prompt_text = get_prompt(args.prompt)
    print(f"Prompt loaded: '{prompt_text}'")

    base64_image = encode_image(args.image)

    api_response = send_request(prompt_text, base64_image)

    llm_output = api_response['choices'][0]['message']['content']

    print("\n=== LLM Response ===\n")
    print(llm_output)
    print("\n====================\n")

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(llm_output)
        print(f"Response saved to {args.output}")

if __name__ == "__main__":
    main()