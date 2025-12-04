import requests
import json
import sys
import time
import os

# --- Configuration ---
# Termux uses ANSI escape codes for color output.
COLOR_GREEN = "\033[92m"
COLOR_BLUE = "\033[94m"
COLOR_RESET = "\033[0m"
MODEL_NAME = "gemini-2.5-flash-preview-09-2025"
API_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/"
MAX_RETRIES = 3
INITIAL_DELAY = 1  # seconds
# ---------------------

def get_api_key():
    """Retrieves the API key from the environment variable."""
    # Check if the API key is provided via the environment variable
    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key:
        print(f"{COLOR_BLUE}--- SETUP REQUIRED ---{COLOR_RESET}", file=sys.stderr)
        print("Error: GEMINI_API_KEY environment variable not found.", file=sys.stderr)
        print("Please export your API key in your shell config (e.g., ~/.zshrc):", file=sys.stderr)
        print(f"export GEMINI_API_KEY='YOUR_KEY_HERE'", file=sys.stderr)
        sys.exit(1)
    return api_key

def generate_content(prompt, api_key):
    """Calls the Gemini API with Google Search grounding and exponential backoff."""
    
    url = f"{API_ENDPOINT}{MODEL_NAME}:generateContent?key={api_key}"
    
    # --- FINAL STRICT SYSTEM INSTRUCTION ---
    # Forces a two-line output: Explanation + Explicit Command Template.
    system_instruction = "You are a helpful and extremely concise Linux command line assistant for Termux. Always answer with a single sentence explanation first. If the question asks for a command, the next line MUST contain the full command template using placeholder variables (e.g., 'mv current_name new_name'). Do not use Markdown code blocks or extra formatting."
    
    payload = {
        "contents": [{ "parts": [{ "text": prompt }] }],
        "tools": [{ "google_search": {} }], # Enable Google Search for current info
        "systemInstruction": { "parts": [{ "text": system_instruction }] },
    }
    
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.post(
                url, 
                headers={'Content-Type': 'application/json'}, 
                data=json.dumps(payload),
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            candidate = result.get('candidates', [{}])[0]
            
            # Extract Text
            text = candidate.get('content', {}).get('parts', [{}])[0].get('text', 'No response text found.')

            # Extract Sources
            sources = []
            grounding_metadata = candidate.get('groundingMetadata', {})
            attributions = grounding_metadata.get('groundingAttributions', [])
            
            for attr in attributions:
                web = attr.get('web', {})
                if web and web.get('title') and web.get('uri'):
                    sources.append(f"{web['title']} ({web['uri']})")

            return text, sources
            
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error on attempt {attempt + 1}: {e}", file=sys.stderr)
        except requests.exceptions.RequestException as e:
            print(f"Network Error on attempt {attempt + 1}: {e}", file=sys.stderr)
        except Exception as e:
            print(f"An unexpected error occurred: {e}", file=sys.stderr)
            
        if attempt < MAX_RETRIES - 1:
            delay = INITIAL_DELAY * (2 ** attempt)
            time.sleep(delay)
        else:
            print("Failed to get a response after maximum retries.", file=sys.stderr)
            sys.exit(1)
            
    return "Error: Could not retrieve a response from the API.", []


def main():
    if len(sys.argv) < 2:
        print("Usage: ai <question>", file=sys.stderr)
        print("Example: ai 'What is the command for renaming a file?'", file=sys.stderr)
        sys.exit(1)
        
    prompt = " ".join(sys.argv[1:])
    api_key = get_api_key()
    
    # Show loading message
    print("🤖 Thinking...", end='\r')
    sys.stdout.flush()
    
    text, sources = generate_content(prompt, api_key)
    
    # Clear "Thinking..." message
    print(" " * 20, end='\r') 
    
    # Print Answer
    print(f"\n{COLOR_GREEN}>>> Gemini Response:{COLOR_RESET}")
    print(text)
    
    # Print Sources
    if sources:
        print(f"\n{COLOR_BLUE}--- Sources ---{COLOR_RESET}")
        for source in sources:
            print(f"  * {source}")
    print()

if __name__ == '__main__':
    # Ensure requests is installed (Termux may not have it by default)
    try:
        import requests
    except ImportError:
        print("The 'requests' library is not installed.", file=sys.stderr)
        print("Run: pip install requests", file=sys.stderr)
        sys.exit(1)
        
    main()
