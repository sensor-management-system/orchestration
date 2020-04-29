import os
import sys
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_rest_jsonapi import Api, ResourceList

#init the app
app = Flask(__name__)

#set config
app_settings = os.getenv('APP_SETTINGS')
app.config.from_object(app_settings)

# instantiate the db
db = SQLAlchemy(app)


# model user to test the db
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)

    def __init__(self, username, email):
        self.username = username
        self.email = email

# test to ensure the proper config was loaded
#print(app.config, file=sys.stderr)

class Ping(ResourceList):
    def get(self):
        response = {
            'status': 'success',
            'message': 'Hello Sensor!'
            }
        return response

api = Api(app)
api.route(Ping, 'test_connection', '/ping')
