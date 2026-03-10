import os
import subprocess
from google.genai import types


schema_run_python_file = types.FunctionDeclaration(
    name='run_python_file',
    description='Safely executes a specified Python file within the permitted working directory, capturing its standard output and error streams while enforcing a timeout and path restrictions',
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description='he relative path to the target file, starting from the current working directory. It must stay within the permitted directory structure and cannot be an absolute path or use ".." to escape the root.'
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                nullable=True,
                description='An optional list of string arguments to be passed to the Python script during execution. Each element in the array represents a command-line argument.'
            )
        },
        required=['file_path']
    )
)


def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(
            os.path.join(working_directory, file_path))

        valid_target_dir = os.path.commonpath(
            [working_dir_abs, target_file]) == working_dir_abs

        if not valid_target_dir:
            return f'  Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return f'  Error: "{file_path}" does not exist or is not a regular file'
        if not target_file.endswith('.py'):
            return f'  Error: "{file_path}" is not a Python file'

        command = ['python3', target_file]
        if args:
            command.extend(args)

        process = subprocess.run(
            command, capture_output=True, text=True, timeout=30000)

        if process.returncode != 0:
            return f'Process exited with code {process.returncode}'
        if not process.stdout and not process.stderr:
            return f'No output produced'

        return f'STDOUT: {process.stdout}\nSTDERR: {process.stderr}'

    except Exception as e:
        return f'Error: executing Python file: {e}'
