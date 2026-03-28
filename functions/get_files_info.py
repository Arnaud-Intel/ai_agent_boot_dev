import os
from google import genai
from google.genai import types as google_types


def get_files_info(working_directory, directory="."):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

        if not valid_target_dir:
            raise Exception(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
        elif not os.path.isdir(target_dir):
            raise Exception(f'Error: "{directory}" is not a directory')

        print(f"--- Path Setup ---")
        print(f"Working Dir (Abs): {working_dir_abs}")
        print(f"Target Dir:        {target_dir}")
        print(f"Is Valid Target?   {valid_target_dir}")

        files = os.listdir(target_dir)
        print(f"\n--- Directory Contents ---")
        print(f"Found {len(files)} items: {files}")


        for file in files: 
            file_with_path = os.path.normpath(os.path.join(target_dir, file))
            size = os.path.getsize(file_with_path)
            dir_verif = os.path.isdir(file_with_path)
            print(f"{file}: filze_size={size} bytes, is_dir={dir_verif}")

    except Exception as e:
        print(f"Unexpected error: {e}")


schema_get_files_info = google_types.FunctionDeclaration(
        name="get_files_info",
        description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
        parameters=google_types.Schema(
            type=google_types.Type.OBJECT,
            properties={
                "directory": google_types.Schema(
                    type=google_types.Type.STRING,
                    description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
                ),
            },
        ),
)