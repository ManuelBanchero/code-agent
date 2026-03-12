from model.Tool.Tool import Tool
from model.Tool.Schema import Schema
import os


class GetFilesInfo(Tool):
    def __init__(self, working_directory):
        super().__init__(working_directory)
        self._schema = Schema(
            name='get_files_info',
            descripcion='Lists files in a specified directory relative to the working directory, providing file size and directory status',
            directory={
                'type': 'string',
                'description': 'Directory path to list files from, relative to the working directory (default is the working directory itself)',
                'required': False
            }
        )

    def get_schema(self):
        return self._schema.get_schema()

    def execute(self, directory='.'):
        try:
            working_dir_abs = os.path.abspath(self._working_directory)
            target_dir = os.path.normpath(
                os.path.join(self._working_directory, directory))

            valid_target_dir = os.path.commonpath(
                [working_dir_abs, target_dir]) == working_dir_abs

            if not valid_target_dir:
                return f'  Error: Cannot list "{directory}" as it is outside the permitted working directory'
            if not os.path.isdir(target_dir):
                return f'  Error: "{directory}" is not a directory'

            files = os.listdir(target_dir)

            dir_data = []
            for file in files:
                if file == "__pycache__" or file.startswith("."):
                    continue

                file_path = os.path.join(target_dir, file)
                file_size = os.path.getsize(file_path)
                is_dir = os.path.isdir(file_path)

                dir_data.append((file, file_size, is_dir))

            data_formated = list(map(
                lambda data: f'- {data[0]}: file_size={data[1]}, is_dir={data[2]}',
                dir_data
            ))
            return '\n  '.join(data_formated)
        except Exception as e:
            return f'  Error: {e}'
