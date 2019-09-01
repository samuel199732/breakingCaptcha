from application.CaptchaResolver import quebra_captcha_base


class Resolve(quebra_captcha_base.ResolverCapcha):

    def __init__(self):
        super(Resolve, self).__init__('captcha02/modelo/frozen_inference_graph.pb',
                                              'captcha02/label/labelmap.pbtxt', 63)
