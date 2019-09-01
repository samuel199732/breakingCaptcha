from application.Request import Validation
from application.Rules import interface
import boto3
import base64
import os
import abc


class AbstractCapctha(interface.InterfaceCaptcha, metaclass=abc.ABCMeta):

    def __init__(self):
        self.Validation = Validation.Validation()
        self.bucket = boto3.resource('s3').Bucket('captchas-para-resolver')

    def delete_file(self, file_name):
        if os.path.exists(file_name):
            os.remove(file_name)

    def decode_base_64(self, base64s):
        return base64.b64decode(base64s)

    def encode_base_64(self, file_name):
        with open(file_name, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        return str(encoded_string, 'utf-8')

    def save_file_s3(self, filename, data):
        self.bucket.put_object(Key=filename, Body=data)

    def execute_save_s3(self, data):
        self.Validation.validator(data)
        imgdata = self.decode_base_64(data['captcha'])
        file = self.save_file(imgdata)
        self.save_file_s3(file, imgdata)
        self.delete_file(file)
