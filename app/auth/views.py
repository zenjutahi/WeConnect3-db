from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

from . import auth
from flask_jwt_extended import get_raw_jwt, jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt
from app.models import User, TokenBlacklist
from app.view_helpers import validate_email, check_json, token_generator
from app.utils import validate_auth_data_null
from app import create_app

@auth.route('/register', methods=['POST'])
def register():

    if check_json():
        data = request.get_json()
        email = validate_auth_data_null(data.get('email'))   
        username = validate_auth_data_null(data.get('username'))
        first_name = validate_auth_data_null(data.get('first_name'))
        password = validate_auth_data_null(data.get('password'))

        if not username or not email or not password:
            return jsonify(
                    {'message':'Invalid Username or password'}), 400
        else:
            if validate_email(email):
                existant_user = User.query.filter_by(email=email).first()
                if not existant_user:
                    new_user = User(email=email, username=username,first_name=first_name,
                                    password=password)
                    new_user.save()
                    return jsonify(
                        {'message': 'New user Succesfully created'}), 201
                return jsonify(
                        {'message': 'This email is registered, login instead'}), 404

            return jsonify(
                    {'message':'Invalid Email. Enter valid email to register'}), 400

    return jsonify(
            {'message':'Bad Request. Request should be JSON format'}), 405


@auth.route('/login', methods=['POST'])
def login():

    if check_json():
        data = request.get_json()
        email = validate_auth_data_null(data.get('email'))   
        password = validate_auth_data_null(data.get('password'))

        if not email or not password:
            return jsonify(
                    {'message':'Enter Valid Data: Email and password'}), 400
        else:
            user = User.query.filter_by(email=email).first()
            print('Hellow owrld', password, user.password)
            if user and user.verify_password(password):
                current_user = user.id
                return token_generator(current_user)
            return jsonify(
                    {'message':'Invalid Password or Email: Enter right credentions to login'}), 401

    return jsonify(
            {'message':'Bad Request. Request should be JSON format'}), 405


@auth.route('/logout', methods=['DELETE'])
@jwt_required
def logout():
    """ logout a user """
    jti = get_raw_jwt()['jti']
    user_identity = get_jwt_identity()
    tokenlist = TokenBlacklist(token=jti, user_identity=user_identity)
    tokenlist.save()
    return jsonify(
        {'message':'User Successfully logged out'}), 200


@auth.route('/resetpassword', methods=['PUT'])
@jwt_required
def reset_password():

    if check_json():
        data = request.get_json()
        old_password = validate_auth_data_null(data.get('old_password'))   
        new_password = validate_auth_data_null(data.get('new_password'))
        jti = get_raw_jwt()['jti']
        print(old_password)


        if not old_password or not new_password :
            return jsonify(
                    {'message':'Enter Valid Data: Email and password'}), 400
        else:
            current_user = get_jwt_identity()
            user = User.query.filter_by(id=current_user).first()
            if user.verify_password(old_password):
                User.update(User, current_user, password=new_password)
                tokenlist = TokenBlacklist(token=jti, user_identity=current_user)
                tokenlist.save()
                return jsonify(
                        {'message':'Password Successfully Changed'}), 200
            return jsonify(
                    {'message':'Enter Valid Password: Old password is wrong'}), 400

    return jsonify(
            {'message':'Bad Request. Request should be JSON format'}), 405
