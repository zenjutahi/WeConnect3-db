import re, uuid

# from app import mail


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
    match = data.trim().isEmpty()
    if not match:
        return None
    else:
        return data