from config.config import WORKING_DIRECTORY, MAX_MODEL_CALLS, AI_MODEL
from utils.prompts import system_prompt
from model.Tool.GetFilesInfo import GetFilesInfo
from model.Agent import Agent
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.environ.get('GEMINI_API_KEY')
if api_key == None:
    raise RuntimeError('The api key must be included on the .env file')

get_files_info = GetFilesInfo(working_directory=WORKING_DIRECTORY)

tools = {
    'get_files_info': get_files_info
}

agent = Agent(
    system_prompt=system_prompt,
    MAX_MODEL_CALLS=MAX_MODEL_CALLS,
    tools=tools,
    ai_model=AI_MODEL,
    API_KEY=api_key
)

agent.query('get the files info about this directory')
