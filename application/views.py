from index import app
from flask import jsonify


@app.route('/')
def index():
    return jsonify({'message': 'API que quebra captcha01!'})
