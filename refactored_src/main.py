from config.config import WORKING_DIRECTORY, MAX_MODEL_CALLS, AI_MODEL, MAX_CHARS
from utils.prompts import system_prompt
from model.Tool.GetFilesInfo import GetFilesInfo
from model.Tool.GetFileContent import GetFileContent
from model.Tool.WriteFile import WriteFile
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
write_file = WriteFile(working_directory=WORKING_DIRECTORY)


tools = {
    'get_files_info': get_files_info,
    'get_file_content': get_file_content,
    'write_file': write_file
}

agent = Agent(
    system_prompt=system_prompt,
    MAX_MODEL_CALLS=MAX_MODEL_CALLS,
    tools=tools,
    ai_model=AI_MODEL,
    API_KEY=api_key
)

response, success = agent.query(
    'modify lorem.txt and write: "This is a new test."')
if success:
    print(response)
else:
    print(response)
    exit(1)
