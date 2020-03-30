from flask import Flask, jsonify
import os
import sys

#init the app
app = Flask(__name__)

#set config
app_settings = os.getenv('APP_SETTINGS')
app.config.from_object(app_settings)

# test to ensure the proper config was loaded
print(app.config, file=sys.stderr)
@app.route('/user/ping', methods=['GET'])
def ping_pong():
    return jsonify\
    ({
            'status':'success',
            'message':'Pong'
    })