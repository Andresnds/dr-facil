from flask import Flask

app = Flask(__name__)
app.config.from_object('config')

import mongoengine
mongoengine.connect('dr_facil', host=app.config['MONGOLAB_URI'])

import views