import os

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
        with open(target_abs, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"