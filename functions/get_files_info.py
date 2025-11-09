import os
import os.path
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

def get_files_info(working_directory, directory="."):
    try:
        # Building the full path
        full_path = os.path.join(working_directory, directory)
        
        # Resolve to absolute paths and follow symlinks for security
        working_abs = os.path.realpath(working_directory)
        target_abs = os.path.realpath(full_path)
        
        # Validating boundaries
        if not target_abs.startswith(working_abs):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        # Checking if the target is a directory
        if not os.path.isdir(target_abs):  
            return f'Error: "{directory}" is not a directory'
        
        items = os.listdir(target_abs)
        result_lines = []
            
        for item in items:
            item_path = os.path.join(target_abs, item)
            size = os.path.getsize(item_path)
            is_directory = os.path.isdir(item_path)
            line = f"- {item}: file_size={size} bytes, is_dir={is_directory}"
            result_lines.append(line)

            
        return "\n".join(result_lines)
            
    except Exception as e:
        return f"Error: {str(e)}"
