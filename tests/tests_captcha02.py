import unittest
from application.Rules.SamuelRulesCaptcha02 import rules
from application.Request import Validation
from cerberus import SchemaError
import binascii
import os


class TestCaptcha02Methods(unittest.TestCase):
    rules = rules.SamuelRulesCaptcha02()
    validator = Validation.Validation()

    def test_captcha_resolve(self):
        request = {'captcha': self.rules.encode_base_64("tests/imagem_exemplo_captcha02.captcha")}
        string = self.rules.execute_resolve_captcha(request)
        self.assertEqual(string, 't2B2H')

    def test_validator_request(self):
        request = {'captcha': self.rules.encode_base_64("tests/imagem_exemplo_captcha02.captcha")}
        self.assertTrue(self.validator.validator(request))

    def test_image_save(self):
        request = {'captcha': self.rules.encode_base_64("tests/imagem_exemplo_captcha02.captcha")}
        image = self.rules.decode_base_64(request['captcha'])
        file_name = self.rules.save_file(image)
        self.assertTrue(os.path.exists(file_name))
        self.rules.delete_file(file_name)

    def test_delete_image(self):
        request = {'captcha': self.rules.encode_base_64("tests/imagem_exemplo_captcha02.captcha")}
        image = self.rules.decode_base_64(request['captcha'])
        file_name = self.rules.save_file(image)
        self.rules.delete_file(file_name)
        self.assertFalse(os.path.exists(file_name))

    def test_error_request_sem_parametros(self):
        request = {}
        with self.assertRaises(SchemaError):
            self.validator.validator(request)

    def test_error_request_vazia(self):
        request = {'captcha': ""}
        with self.assertRaises(SchemaError):
            self.validator.validator(request)

    def test_error_base64_invalido(self):
        request = {'captcha': self.rules.encode_base_64("tests/imagem_exemplo_captcha02.captcha")[1:]}
        with self.assertRaises(TypeError):
            self.rules.decode_base_64(request)

        with self.assertRaises(binascii.Error):
            self.rules.execute_resolve_captcha(request)


if __name__ == '__main__':
    unittest.main()
