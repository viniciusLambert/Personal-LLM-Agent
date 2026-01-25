import os
from config import MAX_CHARS
from google.genai import types

def get_llm_schema_files_content():
    return types.FunctionDeclaration(
        name="get_file_content",
        description="get file content, from a file in a specified directory relative to the working directory",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "working_directory": types.Schema(
                    type=types.Type.STRING,
                    description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
                ),
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="file name, from the file present on the directory, that we want the content"
                ),
            },
        ),
    )

def get_file_content(working_directory, file_path):
    try:
        working_dir_abs = os.path.abspath(working_directory) 
        target_file = os.path.normpath(
            os.path.join(working_dir_abs, file_path)
        )

        is_a_valid_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs 

        if not is_a_valid_file:
            raise Exception(
                f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
            )
        
        if not os.path.exists(target_file) or not os.path.isfile(target_file):
            raise Exception(
                f'Error: File not found or is not a regular file: "{file_path}"'
            )

        with open(target_file, "r") as f:
            file_content_string = f.read(MAX_CHARS)

            if f.read(1):
                file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            return file_content_string
        return ''
    except Exception as e:
        return f'Error: {e}'

    
