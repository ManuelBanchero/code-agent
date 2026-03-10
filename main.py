import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse
from prompts import system_prompt
from call_function import available_functions, call_function

load_dotenv()
api_key = os.environ.get('GEMINI_API_KEY')
if api_key == None:
    raise RuntimeError('The api key must be included on the .env file')

client = genai.Client(api_key=api_key)


def main():
    parser = argparse.ArgumentParser(description='Code Agent')
    parser.add_argument('user_prompt', type=str, help='User prompt')
    parser.add_argument('--verbose', action='store_true',
                        help='Enable verbose output')
    args = parser.parse_args()

    messages = [types.Content(
        role="user", parts=[types.Part(text=args.user_prompt)])]

    for _ in range(20):
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt
            )
        )

        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)

        if not response.usage_metadata:
            raise RuntimeError(
                'An unexpected error has ocurred trying to make a request to Gemini')

        if args.verbose:
            print(f'User prompt: {args.user_prompt}')
            prompt_tokens = response.usage_metadata.prompt_token_count
            response_tokens = response.usage_metadata.candidates_token_count
            print(f'Prompt tokens: {prompt_tokens}')
            print(f'Response tokens: {response_tokens}')

        function_results = []
        if response.function_calls:
            for function in response.function_calls:
                call_function_obj = call_function(function, True)
                if len(call_function_obj.parts) == 0 or not call_function_obj.parts:
                    raise Exception('Function response has an empty list')

                function_response = call_function_obj.parts[0].function_response
                if not function_response:
                    raise Exception('We expected an FunctionResponse object')

                if not function_response.response:
                    raise Exception('The response is a None value')

                # Add the result to a list
                function_results.append(call_function_obj.parts[0])
                messages.append(types.Content(
                    role='user', parts=function_results))

                if args.verbose:
                    print(
                        f'{call_function_obj.parts[0].function_response.response}')
        else:
            print(response.text)
            return

    print('The AI Agent has excedeed of the maximum amount of calls')
    exit(1)


if __name__ == "__main__":
    main()
