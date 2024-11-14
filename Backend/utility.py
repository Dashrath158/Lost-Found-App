from flask import Blueprint, jsonify, request, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from models.User import User
from models import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

user_api = Blueprint('utility', __name__)  # Define the Blueprint