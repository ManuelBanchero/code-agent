from model.Tool.Tool import Tool
from model.Tool.Schema import Schema
import os


class WriteFile(Tool):
    def __init__(self, working_directory):
        super().__init__(working_directory)
        self._schema = Schema(
            name='write_file',
            descripcion='Writes text content to a specified file path, automatically creating any missing parent directories and ensuring the operation stays within the permitted working directory',
            file_path={
                'type': 'string',
                'description': 'he relative path to the target file, starting from the current working directory. It must stay within the permitted directory structure and cannot be an absolute path or use ".." to escape the root.',
                'required': True
            },
            content={
                'type': 'string',
                'description': 'The text data to be written into the file. The function will overwrite any existing content in the file with this new string.',
                'required': True
            }
        )

    def get_schema(self):
        return self._schema.get_schema()

    def execute(self, file_path, content):
        try:
            working_dir_abs = os.path.abspath(self._working_directory)
            target_file = os.path.normpath(
                os.path.join(self._working_directory, file_path))

            valid_target_dir = os.path.commonpath(
                [working_dir_abs, target_file]) == working_dir_abs

            if not valid_target_dir:
                return f'  Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
            if os.path.isdir(target_file):
                return f'  Error: Cannot write to "{file_path}" as it is a directory'

            os.makedirs(os.path.dirname(target_file), exist_ok=True)

            with open(target_file, 'w') as f:
                f.write(content)

            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        except Exception as e:
            return f'Error: {e}'
