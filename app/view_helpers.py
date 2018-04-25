import datetime
from flask import request, jsonify
from flask_jwt_extended import create_access_token, decode_token
from app.utils import check_email



def validate_email(email):
    """Returns True if email is valid"""
    if not check_email(email):
        return False
    return True

def check_json():
    """Returns True if request is json"""
    if request.get_json(silent=True) is None:
        return False
    return True

def token_generator(current_user, expire_time=datetime.timedelta(minutes=30)):
    """Returns access token and response to User"""
    response = {
        'message': 'Successfully Loged In',
        'access_token': create_access_token(identity=current_user, expires_delta=expire_time)

    }
    return jsonify(response), 200