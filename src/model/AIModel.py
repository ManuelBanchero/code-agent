from google import genai
from google.genai import types
import copy


class AIModel:
    def __init__(self, model, API_KEY):
        self.__client = genai.Client(api_key=API_KEY)
        self.__model = model

    # PUBLIC METHODS
    def format_user_prompt(self, user_prompt):
        return types.Content(
            role='user',
            parts=[types.Part(text=user_prompt)]
        )

    def get_chat_complation(self, messages, config):
        # Format config (for use it in a Gemini AI SDK)
        config_formated = self.__format_config(config)

        response = self.__get_response(messages, config=config_formated)

        if not response.usage_metadata:
            raise RuntimeError(
                'An unexpected error has ocurred trying to make a request to Gemini')

        return {
            'prompt_tokens': response.usage_metadata.prompt_token_count,
            'response_tokens': response.usage_metadata.candidates_token_count,
            'candidates': response.candidates,
            'function_calls': response.function_calls,
            # If the model wants to call a function, response has not a text property yet
            'response': None if response.function_calls else response.text
        }

    def get_tool_context(self, tool_name, tool_result):
        tool_context = types.Content(
            role='tool',
            parts=[
                types.Part.from_function_response(
                    name=tool_name,
                    response=tool_result
                )
            ]
        )

        if len(tool_context.parts) == 0 or not tool_context.parts:
            raise Exception('Function response has an empty list')

        if not tool_context.parts[0].function_response:
            raise Exception('We expected an FunctionResponse object')
        if not tool_context.parts[0].function_response.response:
            raise Exception('The response is a None value')

        return tool_context.parts[0]

    def format_tools_result(self, tools_result):
        return types.Content(
            role='user', parts=tools_result
        )

    # PRIVATE METHODS
    def __format_config(self, config):
        schemas = config['tools_schema']
        formated_schemas = list(
            map(lambda schema: self.__format_schema(schema), schemas))

        available_functions = types.Tool(
            function_declarations=formated_schemas
        )

        updated_config = copy.deepcopy(config)
        updated_config['tools_schema'] = available_functions

        return updated_config

    def __format_schema(self, schema):
        # List of iterables values
        iterables_values = ['array']
        properties_values = {}
        required_properties = []

        for property in schema['parameters']:
            value_type = schema['parameters'][property]['type']
            # items_type exists only if value_type is an iterable
            items_type = schema['parameters'][property]['items_type'] if 'items_type' in schema['parameters'][property] else None
            description = schema['parameters'][property]['description']
            required = schema['parameters'][property]['required']
            nullable = schema['parameters'][property]['nullable'] if 'nullable' in schema['parameters'][property] else None

            properties_values[property] = types.Schema(
                type=self.__get_property_type(value_type),
                description=description,
                items=types.Schema(type=self.__get_property_type(
                    items_type)) if value_type in iterables_values else None,
                nullable=nullable
            )

            if required:
                required_properties.append(property)

        return types.FunctionDeclaration(
            name=schema['name'],
            description=schema['description'],
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties=properties_values,
                required=required_properties
            )
        )

    def __get_property_type(self, value_type):
        if value_type.upper() == 'STRING':
            return types.Type.STRING
        elif value_type.upper() == 'ARRAY':
            return types.Type.ARRAY
        else:
            raise Exception(f'The value type "{value_type}" does not exists')

    def __get_response(self, messages, config):
        return self.__client.models.generate_content(
            model=self.__model,
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[config['tools_schema']],
                system_instruction=config['system_prompt']
            )
        )
