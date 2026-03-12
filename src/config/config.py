from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.environ.get('GEMINI_API_KEY')
if api_key == None:
    raise RuntimeError('The api key must be included on the .env file')
MAX_CHARS = 10_000
WORKING_DIRECTORY = '/Users/manuelbanchero/dev/courses/boot_dev/code-agent/calculator'
MAX_MODEL_CALLS = 20
AI_MODEL = 'gemini-2.5-flash'
API_KEY = api_key
