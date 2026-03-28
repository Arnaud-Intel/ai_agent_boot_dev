import os
from config import *

def get_file_content(working_directory, file_path):
    try:
        working_file_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_file_abs, file_path))
        valid_target_file = os.path.commonpath([working_file_abs, target_file]) == working_file_abs

        if not valid_target_file:
            raise Exception(f'Error: Cannot read "{file_path}" as it is outside the permitted working directory')
        elif not os.path.isfile(target_file):
            raise Exception(f'Error: File not found or is not a regular file: "{file_path}"')
    
        with open(target_file, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if f.read(1):
                file_content_string += f'[...File "{target_file}" truncated at {MAX_CHARS} characters]'
            return file_content_string

    except Exception as e:
        print(f"Unexpected error: {e}")