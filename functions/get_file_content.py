import os 
import os.path
import config
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads file's content within the working directory.Will turnacate to 10000 characters if file is too large",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to read, relative to the working directory.",
            ),
        },
        required=["file_path"],
    )
)

def get_file_content(working_directory, file_path):

    full_path = os.path.join(working_directory, file_path)
    # Convert to absolute paths
    working_abs = os.path.abspath(working_directory)
    target_abs = os.path.abspath(full_path)
        
    # Validating boundaries
    if not target_abs.startswith(working_abs):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    # Checking if the target is a directory
    if not os.path.isfile(target_abs):  
        return f'Error: File not found or is not a regular file: "{file_path}"'
   
    try:
        with open(target_abs, "r", encoding="utf-8") as f:
            chunk = f.read(config.MAX_CHARS + 1)
        if len(chunk) <= config.MAX_CHARS:
            return chunk
        return chunk[:config.MAX_CHARS] + f'[...File "{file_path}" truncated at {config.MAX_CHARS} characters]'
    except FileNotFoundError:
        return f'Error: File not found or is not a regular file: "{file_path}"'
    except PermissionError as e:
        return f'Error: {e}'
    except Exception as e:
        return f'Error: {e}'