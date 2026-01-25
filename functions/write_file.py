import os
from google.genai import types


def get_llm_schema_write_file():
    return types.FunctionDeclaration(
        name="write_file",
        description="Write the content inside a file.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "working_directory": types.Schema(
                    type=types.Type.STRING,
                    description="Directory path to list files from, "
                    "relative to the working directory (default is the working directory itself)",
                ),
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="file name, "
                    "present on the directory, that we want to write"
                ),
                "content": types.Schema(
                    type=types.Type.STRING,
                    description="The content to be writed on file."
                )
            },
        ),
    )






def write_file(working_directory, file_path, content):
    try:
        working_dir_abs = os.path.abspath(working_directory) 
        os.makedirs(working_dir_abs, exist_ok=True)
        
        target_file = os.path.normpath(
            os.path.join(working_dir_abs, file_path)
        )
        
        is_a_valid_file = os.path.commonpath(
                [working_dir_abs, target_file]
            ) == working_dir_abs 

        if not is_a_valid_file:
            raise Exception(
                f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
            )
        
        if os.path.isdir(target_file):
            raise Exception(
                f'Error: Cannot write to "{file_path}" as it is a directory'
            )

        with open(target_file, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    
    except Exception as e:
        return f'Error: {e}'