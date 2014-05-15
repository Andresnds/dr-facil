import os
from flask import Flask

app = Flask(__name__)
app.config.from_object('config')

import views

import mongoengine

mongoengine.connect('test', host=app.config['MONGOLAB_URI'])