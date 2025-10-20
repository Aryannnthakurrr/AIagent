import os
import google.genai.types as types

#potential to enforce max content size in future
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes or overwrites content to a file within the working directory only. Creates parent directories if they do not exist. Doesn't allow writing to file if it's outside the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            ),
        },
        required=["file_path", "content"]
    )
)

def write_file(working_directory, file_path, content):
    full_path = os.path.join(working_directory, file_path)
    working_abs = os.path.abspath(working_directory)
    target_abs = os.path.abspath(full_path)

    try:
        common = os.path.commonpath([working_abs, target_abs])
    except ValueError:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    if common != working_abs:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    parent_dir = os.path.dirname(target_abs)
    try:
        os.makedirs(parent_dir, exist_ok=True)
    except Exception as e:
        return f"Error: {e}"

    try:
        with open(target_abs, "w", encoding="utf-8") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"