import os
from config import MAX_CHARS
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name='get_file_content',
    description='Reads the content of a specific file relative to the working directory, with a safety limit on characters and path restricted to the permitted directory',
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description='he relative path to the target file, starting from the current working directory. It must stay within the permitted directory structure and cannot be an absolute path or use ".." to escape the root.'
            )
        },
        required=['file_path']
    )
)


def get_file_content(working_directory, file_path):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(
            os.path.join(working_directory, file_path))

        valid_target_dir = os.path.commonpath(
            [working_dir_abs, target_file]) == working_dir_abs

        if not valid_target_dir:
            return f'  Error: Cannot list "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return f'. Error: File not found or is not a regular file: "{file_path}"'

        content = None
        with open(target_file) as f:
            content = f.read(MAX_CHARS)

            # If the file is bigger than max characters, if we can read another character
            if f.read(1):
                # Warning message
                content += f'\n[... File "{file_path}" truncated at {MAX_CHARS} characters]'

        return content

    except Exception as e:
        return f'  Error: {e}'
