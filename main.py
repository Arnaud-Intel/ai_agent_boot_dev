import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types as google_types
from prompts import *
from functions.call_functions import *


load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")


if not api_key:
    raise RuntimeError("No valid API key found")
client = genai.Client(api_key=api_key)

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()
# Now we can access `args.user_prompt`

messages = [google_types.Content(role="user", parts=[google_types.Part(text=args.user_prompt)])]

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=messages,
    config=google_types.GenerateContentConfig(
    tools=[available_functions], system_instruction=system_prompt
    )
)

if args.verbose:
    if response.usage_metadata is not None:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    else: 
        raise RuntimeError("No Metadata returned")

if response.function_calls:
    for function_call in response.function_calls:
        print(f"Calling function: {function_call.name}({function_call.args})")
else:
    print(response.text)