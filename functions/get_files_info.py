import os
import os.path

def get_files_info(working_directory, directory="."):
    try:
        # Building the full path
        full_path = os.path.join(working_directory, directory)
        
        # Convert to absolute paths
        working_abs = os.path.abspath(working_directory)
        target_abs = os.path.abspath(full_path)
        
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
