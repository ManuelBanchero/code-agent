from config.config import WORKING_DIRECTORY, MAX_MODEL_CALLS, AI_MODEL, API_KEY
from utils.prompts import system_prompt
from model.Tool.GetFilesInfo import GetFilesInfo
from model.Tool.GetFileContent import GetFileContent
from model.Tool.WriteFile import WriteFile
from model.Tool.RunPythonFile import RunPythonFile
from model.Agent import Agent


def build_agent() -> Agent:
    # Create Tools
    get_files_info = GetFilesInfo(working_directory=WORKING_DIRECTORY)
    get_file_content = GetFileContent(working_directory=WORKING_DIRECTORY)
    write_file = WriteFile(working_directory=WORKING_DIRECTORY)
    run_python_file = RunPythonFile(working_directory=WORKING_DIRECTORY)

    agent_tools = {
        'get_files_info': get_files_info,
        'get_file_content': get_file_content,
        'write_file': write_file,
        'run_python_file': run_python_file
    }

    agent = Agent(
        system_prompt=system_prompt,
        MAX_MODEL_CALLS=MAX_MODEL_CALLS,
        tools=agent_tools,
        ai_model=AI_MODEL,
        API_KEY=API_KEY
    )

    return agent
