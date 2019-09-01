import abc


class InterfaceCaptcha(abc.ABC):

    @abc.abstractmethod
    def save_file_s3(self, file_name, data):
        return

    @abc.abstractmethod
    def save_file(self, imgdata):
        return

    @abc.abstractmethod
    def delete_file(self, file_name):
        return

    @abc.abstractmethod
    def decode_base_64(self, base64s):
        return

    @abc.abstractmethod
    def encode_base_64(self, file_name):
        return

    @abc.abstractmethod
    def execute_save_s3(self, data):
        return

    @abc.abstractmethod
    def execute_resolve_captcha(self, data):
        return
