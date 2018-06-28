# third-party imports
import os
from flask import jsonify
from flask_api import FlaskAPI
from flask_mail import Mail
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import (
    JWTManager)
# local imports
from instance.config import app_config
# db variable initialization
db = SQLAlchemy()
jwt = JWTManager()
mail = Mail()
cors = CORS()


# Initialize the app

def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    db.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)
    cors.init_app(app)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/api/auth')

    from .business import business as business_blueprint
    app.register_blueprint(business_blueprint, url_prefix='/api')

    from .review import review as review_blueprint
    app.register_blueprint(review_blueprint, url_prefix='/api/businesses')

    from app.models import TokenBlacklist

    @app.errorhandler(400)
    def bad_request(error):
        """Error handler for a bad request"""
        return jsonify(dict(error='The Server did not understand' +
                                  ' the request')), 400

    @app.errorhandler(404)
    def not_found(error):
        """Error handler for not found page"""
        return jsonify(dict(error='The Resource requested is not' +
                                    ' available')), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        """Error handler for wrong method to an endpoint"""
        return jsonify(dict(error='The HTTP request Method' +
                                  ' is not allowed')), 405

    @app.errorhandler(500)
    def server_error(error):
        """Error handler for a server failure"""
        return jsonify(dict(error='The server encountered an internal error' +
                                  ' and was unable to' +
                                  ' complete your request')), 500

    @jwt.token_in_blacklist_loader
    def check_token_in_blacklist(decrypted_token):
        """Check if token is blacklisted"""
        jti = decrypted_token['jti']
        blacklist = TokenBlacklist.query.filter_by(token=jti).first()
        if blacklist is None:
            return False
        return blacklist.revoked

    return app



config_name = os.getenv('FLASK_CONFIG')
app = create_app('development')
