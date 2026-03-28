import os

def write_file(working_directory, file_path, content):
    try:
        working_file_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_file_abs, file_path))
        valid_target_file = os.path.commonpath([working_file_abs, target_file]) == working_file_abs

        if not valid_target_file:
            raise Exception(f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory')
        elif os.path.isdir(target_file):
            raise Exception(f'Error: Cannot write to "{file_path}" as it is a directory')
        
        os.makedirs(os.path.dirname(target_file), exist_ok=True)

        with open(target_file, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        print(f"Unexpected error: {e}")