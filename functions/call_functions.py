from google import genai
from google.genai import types as google_types # Alias it to stay safe
from functions.get_files_info import *

available_functions = google_types.Tool(
    function_declarations=[schema_get_files_info],
)