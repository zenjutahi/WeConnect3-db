import datetime

from flask_bcrypt import Bcrypt
from app import db

class MyBaseClass(db.Model):
    """ MyBaseModel contains common artributes to be inherited my other models """
    __abstract__ = True

    def save(self):
        # saves object to database
        db.session.add(self)
        db.session.commit()

    def delete(self):
        # deletes an object
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all(class_name):
        """Queries all from a given class"""
        result = class_name.query.all()
        return result

    @staticmethod
    def update(class_name, row_id, **kwargs):
        """Update selected columns in given row in a table"""
        row = class_name.query.filter_by(id=row_id).first()
        for column in kwargs:
            if column == 'password':
                kwargs[column] = Bcrypt().generate_password_hash(kwargs[column]).decode()
            setattr(row, column, kwargs[column])
        db.session.commit()

class User(MyBaseClass):
    """
    This class represents the User table
    """

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(60), index=True, unique=True, nullable=False)
    username = db.Column(db.String(255), index=True, nullable=False)
    first_name = db.Column(db.String(255), index=True)
    register_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    password = db.Column(db.String(128), nullable=False)

    def __init__(self, email, username, first_name, password):
        """Initialize the user with the user details"""
        self.email = email
        self.username = username
        self.first_name = first_name
        self.password = Bcrypt().generate_password_hash(password).decode()
        self.register_date = datetime.datetime.now()


    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return Bcrypt().check_password_hash(self.password, password)

    def __repr__(self):
        return '<User: {}>'.format(self.username)



class Business(MyBaseClass):
    """
    Create a Business table
    """

    __tablename__ = 'businesses'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200))

    def __init__(self, name, description, category, location, user_id):
        """Initialize the business"""
        self.name = name
        self.description = description
        self.category = category
        self.location = location
        self.user_id = user_id

    def accesible(self):
        """ Returns jsonified data """
        return {
        "Business name" : self.name,
        "Business description": self.description,
        "Business category": self.category,
        "Business location": self.location
        }

    def __repr__(self):
        return '<Business: {}>'.format(self.name)



class Review(MyBaseClass):
    """
    Create a Review table
    """

    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    business_id = db.Column(db.Integer, db.ForeignKey('businesses.id'), nullable=False)
    value = db.Column(db.String(200), nullable=False)
    comments = db.Column(db.String(200))

    def __init__(self, value, comments, business_id, user_id):
        """Initialize the review"""
        self.value = value
        self.comments = comments
        self.user_id = user_id
        self.business_id = business_id

    def accesible(self):
        """ Returns jsonified data """
        return {
        "Review value" : self.value,
        "Review comment": self.comments
        }

    def __repr__(self):
        return '<Review: {}>'.format(self.value)


class TokenBlacklist(MyBaseClass):
    """
    Create a Blacklist Table to store tokens
    """

    __tablename__ = 'tokenBlacklists'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_identity = db.Column(db.String(50), nullable=False)
    token = db.Column(db.String(400), nullable=False)
    revoked = db.Column(db.Boolean, nullable=False, default=True)
    blacklisted_date = db.Column(db.DateTime, nullable=False)

    def __init__(self,token, user_identity):
        """Initialize the review"""
        self.token = token
        self.user_identity = user_identity
        self.blacklisted_date = datetime.datetime.now()

    def __repr__(self):
        return '<Token: {}>'.format(self.token)
