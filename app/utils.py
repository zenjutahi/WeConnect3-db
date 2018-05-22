import re
from app.models import Business
from flask import request, jsonify
from functools import wraps


# from app import mail
def require_json(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if request.method in ("GET", "DELETE"):
            return f(*args, **kwargs)
        # Check for json
        if not check_json():
            return jsonify(
                {'message': 'Bad Request. Request should be JSON format'}), 400
        ret_val = f(*args, **kwargs)
        return ret_val
    return wrapper


def check_json():
    """Returns True if request is json"""
    if request.get_json(silent=True) is None:
        return False
    return True


def business_search(search_params):
    search = search_params.get('q')
    operator = "%" + search + "%"
    subquery = Business.query.filter(Business.name.ilike(operator))
    # .filter(Business.description.ilike(operator))\
    # .filter(Business.category.ilike(operator))\
    # .filter(Business.location.ilike(operator))

    limit = search_params.get('limit')
    page = search_params.get('page')
    subquery = business_pagination(subquery, limit, page)
    return subquery.all()


def business_filter(filter_params):
    """" A filter algorithim """
    subquery = Business.query
    required_fields = ['location', 'name', 'category']
    for filter in filter_params:
        if filter not in required_fields:
            continue
        operator = "%" + filter_params[filter] + "%"
        subquery = subquery.filter(getattr(Business, filter).ilike(operator))

    limit = filter_params.get('limit')
    page = filter_params.get('page')
    subquery = business_pagination(subquery, limit, page)
    return subquery.all()


def business_pagination(subquery, limit, page):
    """ a pagination function """
    limit = int(limit or 2)
    page = int(page or 1)
    offset = (page - 1) * limit
    subquery = subquery.limit(limit).offset(offset)
    return subquery


def check_email(email):
    """Returns true if email is valid email format else false"""
    re_checker = r"(^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,})$)"
    if len(email) < 5 or re.match(re_checker, email) is None:
        return False
    return True


def validate_auth_data_null(data):
    """Returns data if input is valid else none"""
    pattern = r'^[a-zA-Z\d_ ]+[\d\w]{3,}'
    match = re.search(pattern, str(data))
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
            assert 0, field + ' should not be missing'
    return data
