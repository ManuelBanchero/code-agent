from config.config import WORKING_DIRECTORY, MAX_MODEL_CALLS, AI_MODEL, MAX_CHARS
from utils.prompts import system_prompt
from model.Tool.GetFilesInfo import GetFilesInfo
from model.Tool.GetFileContent import GetFileContent
from model.Agent import Agent
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.environ.get('GEMINI_API_KEY')
if api_key == None:
    raise RuntimeError('The api key must be included on the .env file')

get_files_info = GetFilesInfo(working_directory=WORKING_DIRECTORY)
get_file_content = GetFileContent(
    working_directory=WORKING_DIRECTORY, max_chars=MAX_CHARS)

tools = {
    'get_files_info': get_files_info,
    'get_file_content': get_file_content
}

agent = Agent(
    system_prompt=system_prompt,
    MAX_MODEL_CALLS=MAX_MODEL_CALLS,
    tools=tools,
    ai_model=AI_MODEL,
    API_KEY=api_key
)

response, success = agent.query('get main.py content')
if success:
    print(response)
else:
    print(response)
    exit(1)
