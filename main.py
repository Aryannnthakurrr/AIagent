import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


#potential for multi turn conversations in future
#potential for multiple tool calls in a loop to execute complex tasks and multistep plans
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

    system_prompt = """
You are a helpful AI coding agent.
Dont ask follow up questions.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths provided to you will be in the working directory "./calculator".
All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.

If you have been provided with a function call, feel free to call the function directly instead of generating a textual response.
Prefer calling tools directly. Infer sensible defaults when the user intent is clear; don’t ask follow-up questions unless required args are missing or ambiguous.
In case of vague instructions, make your best guess based on user intent.
"""

    available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info, 
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
    ]
)

    #calling the 2.0 flash model and giving it prompt as content
    response = client.models.generate_content(
        model='gemini-2.0-flash-001', 
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),
    )
    
    #Checking if the response contains function calls
    if response.function_calls:
        for function_call_part in response.function_calls:
            tool_content = call_function(function_call_part, verbose=is_verbose)
            if not tool_content.parts or not hasattr(tool_content.parts[0], 'function_response'):
                raise RuntimeError("Function call did not return a valid function response.")
            
            function_response = tool_content.parts[0].function_response.response
            if not function_response:
                raise RuntimeError("Function did not return any result.")
            
            if is_verbose:
                print(f"-> {function_response}")
                

    #prints the textual response from the model
    else: print(response.text)

    if is_verbose:
        print("User prompt:", user_prompt)
        #prints input tokens
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        #prints output tokens
        print("Response tokens:", response.usage_metadata.candidates_token_count)


if __name__ == "__main__":
    main()