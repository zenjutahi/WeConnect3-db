from flask import Blueprint

review = Blueprint('review', __name__)

from . import views