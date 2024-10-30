from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize Flask app, database, and JWT manager
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = '5c303052273cfcb635841b9c86d4a7eef498386af15de38ff5a19bd2aeebb803'  # Change this to a random secret key
db = SQLAlchemy(app)
jwt = JWTManager(app)


# Create database tables
with app.app_context():
    db.create_all()  # Create the database tables

# User Registration Endpoint
@app.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    email = request.json.get('email')

    if User.query.filter_by(username=username).first():
        return jsonify({'msg': 'Username already exists.'}), 400

    hashed_password = generate_password_hash(password, method='sha256')
    new_user = User(username=username, password=hashed_password, email=email)

    new_user.save()  # Use the save method to store the user

    return jsonify({'msg': 'User created successfully!'}), 201

# User Login Endpoint
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        # Create a new access token
        access_token = create_access_token(identity={'username': user.username})
        return jsonify(access_token=access_token), 200

    return jsonify({'msg': 'Invalid credentials!'}), 401

# Protected Route
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user['username']), 200

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
