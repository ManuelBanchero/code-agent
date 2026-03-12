from model.Tool.Tool import Tool
from model.Tool.Schema import Schema
import os
import subprocess


class RunPythonFile(Tool):
    def __init__(self, working_directory):
        super().__init__(working_directory)
        self._schema = Schema(
            name='run_python_file',
            descripcion='Safely executes a specified Python file within the permitted working directory, capturing its standard output and error streams while enforcing a timeout and path restrictions',
            file_path={
                'type': 'string',
                'description': 'he relative path to the target file, starting from the current working directory. It must stay within the permitted directory structure and cannot be an absolute path or use ".." to escape the root.',
                'required': True
            },
            args={
                'type': 'array',
                'items_type': 'string',
                'nullable': True,
                'description': 'An optional list of string arguments to be passed to the Python script during execution. Each element in the array represents a command-line argument.',
                'required': False
            }
        )

    def get_schema(self):
        return super().get_schema()

    def execute(self, file_path, args=None):
        try:
            working_dir_abs = os.path.abspath(self._working_directory)
            target_file = os.path.normpath(
                os.path.join(self._working_directory, file_path))

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
