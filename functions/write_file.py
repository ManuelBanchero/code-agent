import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name='write_file',
    description='Writes text content to a specified file path, automatically creating any missing parent directories and ensuring the operation stays within the permitted working directory',
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description='he relative path to the target file, starting from the current working directory. It must stay within the permitted directory structure and cannot be an absolute path or use ".." to escape the root.'
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description='The text data to be written into the file. The function will overwrite any existing content in the file with this new string.'
            )
        },
        required=['file_path', 'content']
    )
)


def write_file(working_directory, file_path, content):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(
            os.path.join(working_directory, file_path))

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
