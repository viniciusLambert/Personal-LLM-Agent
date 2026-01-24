import os



def get_files_info(working_directory, directory="."):
    try:
        working_dir_abs = os.path.abspath(working_directory) 
        target_dir = os.path.normpath(
            os.path.join(working_dir_abs, directory)
        )

        is_a_valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs 

        if not is_a_valid_target_dir:
            raise Exception(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
        
        if not os.path.exists(target_dir):
            raise Exception(f'Error: "{directory}" is not a directory')
        
        dir_content = os.listdir(target_dir)

        current_directory = 'current' if directory == '.' else f"'{directory}'"
        print(f"Result for {current_directory} directory:")
        for item in dir_content:
            item_dir = target_dir + '/' + item
            is_dir = os.path.isdir(item_dir)
            print(f'- {item}: file_size={os.path.getsize(item_dir)} bytes, is_dir={is_dir}')
    except Exception as e:
        print(f"Error {e}.")