from cerberus import Validator
from cerberus import SchemaError


class Validation:

    def __init__(self):
        self.schema = {'captcha': {'type': 'string', 'required': True, 'empty': False}}

    def validator(self, request):
        rule = Validator(self.schema)
        try:
            if not rule.validate(request):
                raise SchemaError
        except Exception as e:
            raise SchemaError
        return True
