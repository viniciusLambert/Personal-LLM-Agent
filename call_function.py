from functions.get_files_info import get_llm_schema_files_info
from google.genai import types

available_functions = types.Tool(
    function_declarations=[get_llm_schema_files_info()],
)