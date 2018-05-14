import re, uuid
from app.models import Business
from flask import request, jsonify
from functools import wraps

# from app import mail

def require_json(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if request.method in ("GET","DELETE"):
            return f(*args, **kwargs)
        # Check for json
        if not check_json():
            return jsonify(
                {'message':'Bad Request. Request should be JSON format'}), 405
        return f(*args, **kwargs)


    return wrapper

def check_json():
    """Returns True if request is json"""
    if request.get_json(silent=True) is None:
        return False
    return True

def business_search(query):
    pass



def check_email(email):
    """Returns true if email is valid email format else false"""
    re_checker = r"(^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,})$)"
    if len(email) < 5 or re.match(re_checker, email) is None:
        return False
    return True

def validate_auth_data_null(data):
    """Returns data if input is valid else none"""
    pattern = r'^[a-zA-Z_ ]+[\d\w]{3,}'
    match = re.search(pattern, data)
    if not match:
        return None
    else:
        return data

def validate_buss_data_null(data):
    """Returns Data if input is valid else None"""
    data = data.split()
    match = ' '.join(data)
    if not match:
        return None
    else:
        return match

def check_blank_key(data, required_fields):

    for field in required_fields:
        if not data.get(field):
            assert 0, field + ' is Missing'
    return data
