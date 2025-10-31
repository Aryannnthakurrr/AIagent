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
def main():

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

*prioritize getting a files info through get_filies_info before reading files to understand the directory structure.
*prioritize reading files before executing them to understand their content and context.
*perform checks after your attempted fix to verify if the issue is resolved in case of tool calls.
*add clear comments when writing or modifying code to explain your changes.

*important: Make sure to provide a summary of all the actions you took once the task is complete.

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
    counter = 0
    while counter<20:
        try:
            #calling the 2.0 flash model and giving it prompt as content
            response = client.models.generate_content(
                model='gemini-2.0-flash-001', 
                contents=messages,
                config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),
            )
            
            for candidate in response.candidates:
                messages.append(candidate.content)

            #Checking if the response contains function calls
            if response.function_calls:
                for function_call_part in response.function_calls:
                    tool_content = call_function(function_call_part, verbose=is_verbose)
                    if not tool_content.parts or not hasattr(tool_content.parts[0], 'function_response'):
                        print("warning: Function call did not return a valid function response.")
                        continue

                    function_response = tool_content.parts[0].function_response.response 
                    if not function_response:
                        print("warning: Function response is empty.")
                        continue

                    messages.append(
                        types.Content(
                            role="user",
                            parts=[
                                types.Part.from_function_response(
                                    name=function_call_part.name,
                                    response=function_response,
                                )
                            ],
                        )
                    )
                
                if is_verbose:
                    print(f"-> {function_response}")
            else:
                #No function calls, so we assume the agent has completed its task
                print(response.text)
                if is_verbose:
                    print("User prompt:", user_prompt)
                    print("Prompt tokens:", response.usage_metadata.prompt_token_count)
                    print("Response tokens:", response.usage_metadata.candidates_token_count)
                break
        except Exception as e:
            error_str = str(e)
            #Break on quota errors after checking retry delay
            if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                retry_delay = 2 ** counter #exponential retry delay
                if counter >= 3:
                    print(f"Quota exhausted after {counter} retries")
                    break
                print(f"Rate limited.Retrying in {retry_delay}s...(attempt {counter}/3)")
                time.sleep(retry_delay)
            else:
                print("Error occured during agent turn", str(e))
            continue

        counter += 1

        
    


if __name__ == "__main__":
    main()