import os
import argparse
from google import genai
from google.genai import types
from dotenv import load_dotenv



def main():

    args = setup_user_args()
    api_key = get_api_key()
    client = setup_client(api_key=api_key)

    user_prompt = args.user_prompt 
    verbose = args.verbose

    content = generate_content(client=client, user_input=user_prompt)
    print_outputs(user_input=user_prompt, generated_content=content, verbose=verbose)


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

def generate_content(client: genai.Client, user_input:str) -> types.GenerateContentResponse:
    messages = [types.Content(role="user", parts=[types.Part(text=user_input)])] 
    generated_content = client._models.generate_content(
        model='gemini-2.5-flash', 
        contents=messages)

    if not generated_content.usage_metadata:
        raise RuntimeError('api not found')

    return generated_content


def print_outputs(user_input, generated_content=types.GenerateContentResponse, verbose=False):
    if verbose:
        print(f'User prompt: {user_input}')
        print(f'Prompt tokens: {generated_content.usage_metadata.prompt_token_count}') # type: ignore
        print(f'Response tokens: {generated_content.usage_metadata.candidates_token_count}') # type: ignore
    print(generated_content.text)

if __name__ == "__main__":
    main()
