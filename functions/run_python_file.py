import os
import subprocess
import shlex  # <--- Import this to safely parse string arguments
from google import genai
from google.genai import types as google_types

def run_python_file(working_directory, file_path, args=None):
    try:
        working_file_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_file_abs, file_path))
        
        valid_target_file = os.path.commonpath([working_file_abs, target_file]) == working_file_abs

        # FIX 3: Return these error strings to the LLM instead of raising an unhandled exception
        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        elif not target_file.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'
        elif not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        command = ["python", file_path]
        if args:
            # FIX 2: Safely split the string into a list of arguments
            command.extend(shlex.split(args))
        
        result_string = ""

        # FIX 1: Add cwd=working_directory to the subprocess call!
        result = subprocess.run(command, cwd=working_directory, text=True, timeout=30, capture_output=True)
        
        if result.returncode != 0:
            result_string = f"Process exited with code {result.returncode}\n"
            print(result_string)
        
        if not result.stderr and not result.stdout:
            result_string += "No output produced\n"
        else:
            if result.stdout != "":
                result_string += f"STDOUT: {result.stdout}\n"
            
            if result.stderr != "":
                result_string += f"STDERR: {result.stderr}\n"
            
        return result_string
        
    except Exception as e:
        # FIX 3: Return the error so the AI knows what failed
        return f"Error executing Python file: {e}"

schema_run_python_file = google_types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a specified python file relative to the working directory, providing file path, directory status and (optionally) args",
    parameters=google_types.Schema(
        type=google_types.Type.OBJECT,
        properties={
            "file_path": google_types.Schema(
                type=google_types.Type.STRING,
                description="File path to run, relative to the working directory",
            ),
            "args": google_types.Schema(
                type=google_types.Type.STRING,
                description="args for additional instruction for the Python script (optional)",
            ),
        },
    ),
)