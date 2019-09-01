from flask import Flask
from flask_restful import Api

app = Flask(__name__)
api = Api(app)

from application import resources
from application import views
from application import models

api.add_resource(resources.ResolveCaptcha01, '/captcha01')
api.add_resource(resources.CallBackCaptcha01, '/captcha01/callback')
api.add_resource(resources.ResolveCaptcha02, '/captcha02')
api.add_resource(resources.CallBackCaptcha02, '/captcha02/callback')