import os
import subprocess

def run_python_file(working_directory: str, file_path: str, args: list = []):
    full_path = os.path.join(working_directory, file_path)
    working_abs = os.path.abspath(working_directory)
    target_abs = os.path.abspath(full_path)
    
    
    try:
        common = os.path.commonpath([working_abs, target_abs])
    except ValueError:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if common != working_abs:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not target_abs.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'
    
    elif not os.path.isfile(target_abs) :
        return f'Error: File "{file_path}" not found.'
    
    try:
        completed_object = subprocess.run(
            ["python3", target_abs, *args],
            cwd=working_abs,
            timeout=30,
            capture_output=True,
            text=True
        )
        out = (completed_object.stdout or "").strip()
        err = (completed_object.stderr or "").strip()

        if not out and not err:
            return "No output produced."
        
        exit_msg = [f'STDOUT: {out}', f'STDERR: {err}']

        if completed_object.returncode != 0:
            exit_msg.append(f'Process exited with code {completed_object.returncode}')
        return "\n".join(exit_msg)
    
    except Exception as e:
        return f'Error: executing Python file: {e}'
        
        
