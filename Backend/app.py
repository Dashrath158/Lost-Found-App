from flask import Flask
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from models import db
from user_apis import user_api  # Import the Blueprint

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = '5c303052273cfcb635841b9c86d4a7eef498386af15de38ff5a19bd2aeebb803'

db.init_app(app)
jwt = JWTManager(app)

# Register the user_api Blueprint
app.register_blueprint(user_api, url_prefix='/user')  # Routes are now prefixed with /api

with app.app_context():
    db.create_all()  # Create tables if they don't exist

@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user['username']), 200

if __name__ == '__main__':
    app.run(debug=True)
