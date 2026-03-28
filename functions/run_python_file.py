import os
import subprocess

def run_python_file(working_directory, file_path, args=None):
    try:
        working_file_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_file_abs, file_path))
        valid_target_file = os.path.commonpath([working_file_abs, target_file]) == working_file_abs

        if not valid_target_file:
            raise Exception(f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory')
        elif not target_file.endswith('.py'):
            raise Exception(f'Error: "{file_path}" is not a Python file')
        elif not os.path.isfile(target_file):
            raise Exception(f'Error: "{file_path}" does not exist or is not a regular file')

        command = ["python", file_path]
        if args:
            command.extend(args)
        
        result_string = ""

        result = subprocess.run(command, text=True, timeout=30, capture_output=True)
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
        print(f"Error: executing Python file: {e}")