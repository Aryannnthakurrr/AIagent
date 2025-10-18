import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

def main():
    
    #checking if a prompt was entered
    if len(sys.argv) < 2:
        print("Usage: python3 main.py <prompt>")
        sys.exit(1)

    #checking if the prompt had --verbose flag
    is_verbose = '--verbose' in sys.argv

    prompt_args = [arg for arg in sys.argv[1:] if arg != '--verbose']

    #joining the command line arguments into a string
    user_prompt = ' '.join(prompt_args)

    #conversation history with role of user
    messages = [
        types.Content(
            role="user",
            parts=[types.Part(text=user_prompt)]
        )
    ]

    #calling the 2.0 flash model and giving it prompt as content
    response = client.models.generate_content(
        model='gemini-2.0-flash-001', 
        contents=messages
    )
    
    #prints the textual response from the model
    print(response.text)

    if is_verbose:
        print("User prompt:", user_prompt)
        #prints input tokens
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        #prints output tokens
        print("Response tokens:", response.usage_metadata.candidates_token_count)


if __name__ == "__main__":
    main()