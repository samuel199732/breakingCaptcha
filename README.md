# breakingCaptcha

Python >= 3.7

Install Dependencies
```
 pip install -r requirements
```

if you want to improve the models You will need to install manually  the models from tensorflow.

https://github.com/tensorflow/models/tree/master/research/slim

in order to do it. go to research/slim and execute this command
```
protoc object_detection/protos/*.proto --python_out=.
```

if you do not have protoc here is the link to install
http://google.github.io/proto-lens/installing-protoc.html


Running the tests
 
```
python -m unittest -v tests/tests_captcha01.py tests/tests_captcha02.py
```
