import os
import argparse
from google import genai
from google.genai import types
from dotenv import load_dotenv
from prompt import system_prompt
from call_function import available_functions, call_function


def main():

    args = setup_user_args()
    api_key = get_api_key()
    client = setup_client(api_key=api_key)

    user_prompt = args.user_prompt 
    verbose = args.verbose
    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])] 
    MAX_ITERATION = 20
    for i in range(MAX_ITERATION):
        content = generate_content(client=client, messages=messages)
        if content.candidates:
            for cand in content.candidates:
                if cand.content:
                    messages.append(cand.content)
            
        print_outputs(user_input=user_prompt, generated_content=content, verbose=verbose)

        if content.function_calls == None:
            exit(0)
        function_call_results = call_agent_requested_functions(content, verbose=verbose)
        if function_call_results:
            messages.append(types.Content(role="user", parts=function_call_results))
        print(function_call_results)

        if i == MAX_ITERATION - 1:
            print("Fail to find a result")
            exit(1)

def setup_user_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('user_prompt', type=str, help='User prompt')
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    return args

def get_api_key():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")   
    if(api_key == None):
        raise RuntimeError("Gemini API not found")  
    return api_key

def setup_client(api_key):
    client = genai.Client(api_key=api_key)
    return client 

def generate_content(client: genai.Client, messages) -> types.GenerateContentResponse:
    generated_content = client._models.generate_content(
        model='gemini-2.5-flash', 
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt,
            temperature=0
        )    
    )

    if not generated_content.usage_metadata:
        raise RuntimeError('api not found')

    return generated_content

def call_agent_requested_functions(generated_content, verbose=False):
    results = []
    if(generated_content.function_calls):
        for function in generated_content.function_calls:
            result = call_function(function)
            if result.parts and result.parts[0].function_response:
                results.append(result.parts[0])
                if verbose:
                    print(f"-> {result.parts[0].function_response.response}")

    return results

def print_outputs(user_input, generated_content: types.GenerateContentResponse, verbose=False):
    if verbose:
        print_headers(user_input=user_input, usage_metadata=generated_content.usage_metadata)
    print_functions_call(generated_content.function_calls)
    
    print(generated_content.text)

def print_headers(user_input, usage_metadata):
    print(f'User prompt: {user_input}')
    print(f'Prompt tokens: {usage_metadata.prompt_token_count}') # type: ignore
    print(f'Response tokens: {usage_metadata.candidates_token_count}') # type: ignore

def print_functions_call(function_calls):
    if(not function_calls):
        return
    for function_call in function_calls:
        print(f"Calling function: {function_call.name}({function_call.args})")    
    return

if __name__ == "__main__":
    main()
