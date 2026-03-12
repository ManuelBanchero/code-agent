from abc import ABC, abstractmethod


class Tool(ABC):
    def __init__(self, working_directory):
        self._working_directory = working_directory
        self._schema = None

    @abstractmethod
    def execute(self, *args, **kwargs):
        pass

    def get_schema(self):
        return self._schema.get_schema()
