import os
from google import genai
from google.genai import types as google_types

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


schema_write_file = google_types.FunctionDeclaration(
name="write_file",
description="Writes a specified content into a specified file path, providing file path, directory status and content",
parameters=google_types.Schema(
    type=google_types.Type.OBJECT,
    properties={
        "file_path": google_types.Schema(
            type=google_types.Type.STRING,
            description="File path to list files from, relative to the working directory",
        ),
        "content": google_types.Schema(
            type=google_types.Type.STRING,
            description="content to be written into the file",
        ),
    },
),
)