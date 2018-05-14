from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

import datetime
from . import business
from flask_jwt_extended import get_raw_jwt, jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt
from app.models import Business
from app.view_helpers import validate_email,token_generator
from app.utils import check_blank_key, validate_buss_data_null, require_json




@business.route('/businesses', methods=['GET', 'POST'])
@jwt_required
@require_json
def registerBusiness():
    """ This is to register a business"""
    current_user = get_jwt_identity()
    if request.method == 'POST':
        # Check for blank key
        try:
            required_fields = ['name', 'description', 'category', 'location']
            data = check_blank_key(request.get_json(), required_fields)
        except AssertionError as err:
            msg = err.args[0]
            return jsonify({"message": msg})
        # Check if user entered a name and location
        name = validate_buss_data_null(data['name'])
        description = validate_buss_data_null(data['description'])
        location = validate_buss_data_null(data['location'])
        category = validate_buss_data_null(data['category'])
        if not location or not description or not name:
            return jsonify(
                {'message': 'You need a business name and location to Register'}), 403
        # Check if business is registered
        exist_business=Business.query.filter_by(name=name).first()
        if exist_business:
            return jsonify(
                {'message': 'This Business is already registered'}), 409

        new_business=Business(name=name, description=description, category=category,
                            location=location, user_id=current_user)
        new_business.save()
        current_business=Business.query.filter_by(user_id=current_user).first()
        new_business_id = current_business.id
        new_business_name = current_business.name

        return jsonify(
            {'message': 'New business has been created',
             'businesses ID': new_business_id,
             'business name': new_business_name
             }), 201

    # Get all businesses
    all_businesses = Business.get_all(Business)
    business_list = []
    for business in all_businesses:
        business_info = business.accesible()
        business_list.append(business_info)
    return jsonify({'message': 'These are the businesses',
                    'businesses': business_list
                    }), 200




@business.route('/businesses/<int:business_id>', methods=['GET', 'PUT', 'DELETE'])
@require_json
@jwt_required
def editBusiness(business_id):
    current_user = get_jwt_identity()
    exist_business=Business.query.filter_by(id=business_id).first()
    # Check if business exists
    if not exist_business:
        return jsonify({'message': 'Bussniess does not exist'}), 404
    if request.method == 'GET':
        business_info = exist_business.accesible()
        return jsonify({'business': business_info,
                        'message': 'Here is the searched business'
                        }), 200
    if current_user != exist_business.user_id:
        return jsonify({'message': 'You can only change your own business'}), 403

    elif request.method == 'DELETE':
        exist_business.delete()
        return jsonify(
            {'message': 'Business successfully deleted'}), 202

    # Check for blank key
    try:
        required_fields = ['name', 'description', 'category', 'location']
        data = check_blank_key(request.get_json(), required_fields)
    except AssertionError as err:
        msg = err.args[0]
        return jsonify({"message": msg})
    # Check for null user data
    name = validate_buss_data_null(data['name'])
    description = validate_buss_data_null(data['description'])
    location = validate_buss_data_null(data['location'])
    category = validate_buss_data_null(data['category'])
    if not name or not description or not location:
        return jsonify(
            {'message': 'Business name and Location have to be entred'}), 403

    exist_name_business=Business.query.filter_by(name=name).first()
    if exist_name_business:
        return jsonify(
            {'message': 'This Business is name is already used'}), 409

    Business.update(Business, current_user, name=name, description=description,
                    location=location, category=category, user_id=current_user)
    display_business=Business.query.filter_by(user_id=current_user).first()
    info = display_business.accesible()
    return jsonify({'New business': info ,
                    'message': 'Business edited successfully'
                    }), 201


@business.route('/businesses/filters', methods=['GET'])
def filtersBusiness():
    filter_by = request.args.get('category', 'location', type=str)
    pass
