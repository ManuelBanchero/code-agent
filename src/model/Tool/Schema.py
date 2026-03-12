""""
    This is the way you must add the properties

    Schema(name, description, property_name={
        'type': type_value,
        'description': property_descripcion,
        'required': True | False
    }, property_name2={
        ...
    })

    IMPORTANT! If type is an array, you can add: 'item_type': type_value

"""


class Schema:
    def __init__(self, name, descripcion, **properties):
        self.__name = name
        self.__description = descripcion
        self.__properties = properties

    def get_schema(self):
        return {
            'name': self.__name,
            'description': self.__description,
            'parameters': dict(self.__properties)
        }
