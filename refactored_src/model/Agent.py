from model.AIModel import AIModel
import copy

# tools_schema=list(map(lambda tool: tools[tool].get_schema(), tools))


# config_properties could be temperature for example.
class Agent:
    def __init__(self, system_prompt, MAX_MODEL_CALLS, tools, ai_model, API_KEY, **config_properties):
        self.__system_prompt = system_prompt
        self.__MAX_MODEL_CALLS = MAX_MODEL_CALLS
        self.__tools = tools
        self.__messages = []
        self.__ai = AIModel(model=ai_model, API_KEY=API_KEY)
        self.__config_properties = dict(config_properties)

    # PUBLIC METHODS
    def query(self, user_prompt):
        return self.__get_response(user_prompt)

    # PRIVATE METHODS
    def __get_response(self, user_prompt):
        # Create array messages
        self.__create_messages(user_prompt)

        config = self.__create_ai_config()
        # Maximum amount of calls the Agent can call the model
        for _ in range(self.__MAX_MODEL_CALLS):
            response = self.__call_model(config)
            if response:
                return response, True

        # If did not return anything in the loop, return an error
        return 'The AI Agent has excedeed of the maximum amount of calls', False

    def __create_messages(self, user_prompt):
        format_prompt = self.__ai.format_user_prompt(user_prompt)
        self.__add_to_messages(format_prompt)

    def __add_to_messages(self, content):
        self.__messages.append(content)

    def __call_model(self, config):
        chat_completion = self.__ai.get_chat_complation(
            self.__messages, config)

        candidates = chat_completion['candidates']
        if candidates:
            new_messages = self.__add_candidates_context(candidates)
            self.__update_messages(new_messages)

        function_calls = chat_completion['function_calls']
        # If the model want to call a function before give a final answer
        if function_calls:
            self.__call_functions(function_calls)
            return None

        # The model has a final answer
        else:
            return chat_completion['response']

    def __call_functions(self, function_calls):
        function_results = []
        for function in function_calls:
            function_name = function.name or ''
            print(f'Calling function: "{function_name}({function.args})"')
            result = self.__call_function(function_name, function.args)
            # Ask to AIModel to create tool context
            context = self.__ai.get_tool_context(function_name, result)
            # Add to function_results
            function_results.append(context)

        functions_results_formated = self.__ai.format_tools_result(
            function_results)
        self.__add_to_messages(functions_results_formated)

    def __call_function(self, function_name, function_args):
        # Verify if the function exists
        if function_name not in self.__tools:
            return {"error": f'Unknown function: {function_name}'}

        # Get function
        function = self.__tools[function_name]
        # Execute function and save the result
        function_result = function.execute(**function_args)
        return {'result': function_result}

    def __add_candidates_context(self, candidates):
        new_messages = copy.deepcopy(self.__messages)
        for candidate in candidates:
            new_messages.append(candidate.content)

        return new_messages

    def __update_messages(self, new_messages):
        self.__messages = new_messages

    def __create_ai_config(self):
        tools_schema = list(
            map(lambda tool: self.__tools[tool].get_schema(), self.__tools))

        return {
            'tools_schema': tools_schema,
            'system_prompt': self.__system_prompt,
            # in case there are not properties
            **(self.__config_properties or {})
        }
