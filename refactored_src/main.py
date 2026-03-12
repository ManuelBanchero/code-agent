from config.config import WORKING_DIRECTORY, MAX_MODEL_CALLS, AI_MODEL
from utils.prompts import system_prompt
from model.Tool.GetFilesInfo import GetFilesInfo
from model.Tool.GetFileContent import GetFileContent
from model.Tool.WriteFile import WriteFile
from model.Tool.RunPythonFile import RunPythonFile
from model.Agent import Agent
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.environ.get('GEMINI_API_KEY')
if api_key == None:
    raise RuntimeError('The api key must be included on the .env file')

get_files_info = GetFilesInfo(working_directory=WORKING_DIRECTORY)
get_file_content = GetFileContent(working_directory=WORKING_DIRECTORY)
write_file = WriteFile(working_directory=WORKING_DIRECTORY)
run_python_file = RunPythonFile(working_directory=WORKING_DIRECTORY)


tools = {
    'get_files_info': get_files_info,
    'get_file_content': get_file_content,
    'write_file': write_file,
    'run_python_file': run_python_file
}

agent = Agent(
    system_prompt=system_prompt,
    MAX_MODEL_CALLS=MAX_MODEL_CALLS,
    tools=tools,
    ai_model=AI_MODEL,
    API_KEY=api_key
)

response, success = agent.query(
    'watch how this project works and make a sum of 6 + 20')
if success:
    print(response)
else:
    print(response)
    exit(1)
