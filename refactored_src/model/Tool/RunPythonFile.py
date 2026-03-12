from model.Tool.Tool import Tool
from model.Tool.Schema import Schema
import os


class RunPythonFile(Tool):
    def __init__(self, working_directory):
        super().__init__(working_directory)
        self._schema = Schema()
