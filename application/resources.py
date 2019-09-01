from flask_restful import Resource, reqparse
from application.Rules.SamuelRulesCaptcha01 import rules as rules_captcha01
from application.Rules.SamuelRulesCaptcha02 import rules as rules_captcha02

from cerberus import SchemaError
import binascii

parser = reqparse.RequestParser()
parser.add_argument('captcha01', help='Erro na validação de Paramentros', required=True)


class ResolveCaptcha01(Resource):
    rules = rules_captcha01.SamuelRulesCaptcha01()

    def post(self):
        try:
            data = parser.parse_args()
            string = self.rules.execute_resolve_captcha(data)
            response = {"status": 200, "captcha01": string}
        except binascii.Error as e:
            response = {"status": 400, "error": "Base64 inválido"}
        except SchemaError as e:
            response = {"status": 400, "error": "Erro na validação de Parametros"}
        except Exception as e:
            print(e)
            response = {"status": 500, "error": "Tente novamente mais tarde"}

        return response


class CallBackCaptcha01(Resource):
    rules = rules_captcha01.SamuelRulesCaptcha01()

    def post(self):
        try:
            data = parser.parse_args()
            self.rules.execute_save_s3(data)
            response = {"status": 200}
        except binascii.Error as e:
            response = {"status": 400, "error": "Base64 inválido"}
        except SchemaError as e:
            response = {"status": 400, "error": "Erro na validação de Paramentros"}
        except Exception as e:
            print(e)
            response = {"status": 500, "error": "Tente novamente mais tarde"}

        return response


class ResolveCaptcha02(Resource):
    rules = rules_captcha02.SamuelRulesCaptcha02()

    def post(self):
        try:
            data = parser.parse_args()
            string = self.rules.execute_resolve_captcha(data)
            response = {"status": 200, "captcha01": string}
        except binascii.Error as e:
            response = {"status": 400, "error": "Base64 inválido"}
        except SchemaError as e:
            response = {"status": 400, "error": "Erro na validação de Paramentros"}
        except Exception as e:
            print(e)
            response = {"status": 500, "error": "Tente novamente mais tarde"}

        return response


class CallBackCaptcha02(Resource):
    rules = rules_captcha02.SamuelRulesCaptcha02()

    def post(self):
        try:
            data = parser.parse_args()
            self.rules.execute_save_s3(data)
            response = {"status": 200}
        except binascii.Error as e:
            response = {"status": 400, "error": "Base64 inválido"}
        except SchemaError as e:
            response = {"status": 400, "error": "Erro na validação de Paramentros"}
        except Exception as e:
            print(e)
            response = {"status": 500, "error": "Tente novamente mais tarde"}

        return response
