# third-party imports
from flask import jsonify
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
# local imports
from instance.config import app_config
# db variable initialization
db = SQLAlchemy()
jwt = JWTManager()


# Initialize the app

def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    db.init_app(app)
    jwt.init_app(app)

    from app import models

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/api/auth')

    from .business import business as business_blueprint
    app.register_blueprint(business_blueprint, url_prefix='/api' )

    from .review import review as review_blueprint
    app.register_blueprint(review_blueprint, url_prefix='/api/businesses' )

    from app.models import TokenBlacklist

    @app.errorhandler(400)
    def bad_request(error):
        """Error handler for a bad request"""
        return jsonify({'message':'The Server did not understand the request'}), 400

    @app.errorhandler(405)
    def method_not_allowed(error):
        """Error handler for wrong method to an endpoint"""
        return jsonify({'message':'Method not allowed'}), 405

    @app.errorhandler(500)
    def server_error(error):
        """Error handler for wrong method to an endpoint"""
        return jsonify({'message':'Database connection failed! Try Again'}), 500
        
    @jwt.token_in_blacklist_loader
    def check_token_in_blacklist(decrypted_token):
        """Check if token is blacklisted"""
        jti = decrypted_token['jti']
        blacklist = TokenBlacklist.query.filter_by(token=jti).first()
        if blacklist is None:
            return False
        return blacklist.revoked

    return app



