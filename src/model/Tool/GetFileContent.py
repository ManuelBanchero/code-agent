from model.Tool.Tool import Tool
from model.Tool.Schema import Schema
from config.config import MAX_CHARS
import os


class GetFileContent(Tool):
    def __init__(self, working_directory):
        super().__init__(working_directory)
        self.__max_chars = MAX_CHARS
        self._schema = Schema(
            name='get_file_content',
            descripcion='Reads the content of a specific file relative to the working directory, with a safety limit on characters and path restricted to the permitted directory',
            file_path={
                'type': 'string',
                'description': 'he relative path to the target file, starting from the current working directory. It must stay within the permitted directory structure and cannot be an absolute path or use ".." to escape the root.',
                'required': True
            }
        )

    def get_schema(self):
        return super().get_schema()

    def execute(self, file_path):
        try:
            working_dir_abs = os.path.abspath(self._working_directory)
            target_file = os.path.normpath(
                os.path.join(self._working_directory, file_path))

            valid_target_dir = os.path.commonpath(
                [working_dir_abs, target_file]) == working_dir_abs

            if not valid_target_dir:
                return f'  Error: Cannot list "{file_path}" as it is outside the permitted working directory'
            if not os.path.isfile(target_file):
                return f'. Error: File not found or is not a regular file: "{file_path}"'

            content = None
            with open(target_file) as f:
                content = f.read(self.__max_chars)

                # If the file is bigger than max characters, if we can read another character
                if f.read(1):
                    # Warning message
                    content += f'\n[... File "{file_path}" truncated at {self.__max_chars} characters]'

            return content

        except Exception as e:
            return f'  Error: {e}'
