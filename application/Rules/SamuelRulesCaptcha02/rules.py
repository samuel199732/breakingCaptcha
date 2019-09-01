from timeit import default_timer as timer
from application.Rules import abstract
from application.CaptchaResolver.Captcha02 import resolveCaptcha


class SamuelRulesCaptcha02(abstract.AbstractCapctha):
    resolve = resolveCaptcha.Resolve()

    def save_file(self, imgdata):
        tempo = timer()
        filename = 'captcha02/captchas/' + str(tempo) + '.png'
        with open(filename, 'wb') as f:
            f.write(imgdata)

        return filename

    def execute_resolve_captcha(self, data):
        self.Validation.validator(data)
        imgdata = self.decode_base_64(data['captcha'])
        file = self.save_file(imgdata)
        string = self.resolve.captch_detection(file)
        self.delete_file(file)
        return string
