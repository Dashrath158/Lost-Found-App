from flask import Blueprint, jsonify, request, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from models.User import User
from models import db
from flask_jwt_extended import create_access_token

user_api = Blueprint('user_api', __name__)  # Define the Blueprint

@user_api.route('/register', methods=['POST'])
def register():
    try:
        username = request.json.get('username')
        password = request.json.get('password')
        email = request.json.get('email')

        # Use current_app.logger to access Flask’s logger without circular imports
        current_app.logger.info(f"Registration attempt for username: {username}")

        if not username or not password or not email:
            current_app.logger.warning("Registration failed: Missing fields")
            return jsonify({'msg': 'Please provide username, password, and email.'}), 400

        if len(password) < 6:
            current_app.logger.warning("Registration failed: Password too short")
            return jsonify({'msg': 'Password must be at least 6 characters long.'}), 400

        if User.query.filter_by(username=username).first():
            current_app.logger.warning(f"Registration failed: Username '{username}' already exists")
            return jsonify({'msg': 'Username already exists.'}), 400
        if User.query.filter_by(email=email).first():
            current_app.logger.warning(f"Registration failed: Email '{email}' already registered")
            return jsonify({'msg': 'Email already registered.'}), 400

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password, email=email)

        try:
            new_user.save()
            current_app.logger.info(f"User '{username}' registered successfully")
            return jsonify({'msg': 'User created successfully!'}), 201
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Registration failed: Database error for user '{username}': {str(e)}")
            return jsonify({'msg': 'An error occurred during registration.', 'error': str(e)}), 500
    except Exception as ex:
        current_app.logger.error(f"Error in registering user: {str(ex)}")
        return jsonify({'msg': 'An internal error occurred.'}), 500

@user_api.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        access_token = create_access_token(identity={'username': user.username})
        return jsonify(access_token=access_token), 200

    return jsonify({'msg': 'Invalid credentials!'}), 401
