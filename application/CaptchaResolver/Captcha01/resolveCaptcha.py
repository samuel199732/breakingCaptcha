from application.CaptchaResolver import quebra_captcha_base


class Resolve(quebra_captcha_base.ResolverCapcha):

    def __init__(self):
        super(Resolve, self).__init__('captcha01/modelo/frozen_inference_graph.pb', 'captcha01/label/labelmap.pbtxt', 37)
