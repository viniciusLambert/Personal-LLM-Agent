import os


def write_file(working_directory, file_path, content):
    try:
        working_dir_abs = os.path.abspath(working_directory) 
        os.makedirs(working_dir_abs, exist_ok=True)
        
        target_file = os.path.normpath(
            os.path.join(working_dir_abs, file_path)
        )
        
        is_a_valid_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs 

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