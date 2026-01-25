import os
import subprocess
from google.genai import types

def get_llm_schema_run_python_file():
    return types.FunctionDeclaration(
        name="run_python_file",
        description="Run a python script",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "working_directory": types.Schema(
                    type=types.Type.STRING,
                    description="The working directory."
                ),
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="file name, "
                    "from the python file present on the directory, that we want to run"
                ),
                "args": types.Schema(
                    type=types.Type.STRING,
                    description="args to pass when call the python function"
                )
            },
        ),
    )

def run_python_file(working_directory, file_path, args=None):
    try:
        if(file_path[-3:] != ".py"):
            raise Exception(
                f'Error: "{file_path}" is not a Python file'
            )
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(
            os.path.join(working_dir_abs, file_path)
        )
        is_a_valid_file = os.path.commonpath(
            [working_dir_abs, target_file]
        ) == working_dir_abs    

        if not is_a_valid_file:
            raise Exception(
                f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
            )
        if not os.path.isfile(target_file):
            raise Exception(
                f'Error: "{file_path}" does not exist or is not a regular file'
            )
        
        
        command = ["python", target_file]
        if(args):
            for arg in args:
                command.extend(arg)

        process = subprocess.run(
            command, 
            cwd=working_dir_abs,
            capture_output=True,
            text=True, 
            timeout=30
        )

        output_string = ""
        if(process.returncode):
            output_string += f"Process exited with code {process.returncode}"

        if(not process.stderr and not process.stdout):
            output_string += "No output produced"
        
        if(process.stderr):
            output_string += f"STDERR: {process.stderr}"
        
        if(process.stdout):
            output_string += f"STDOUT: {process.stdout}"
        
        return output_string

    except Exception as e:
        return  f"Error: {e}"