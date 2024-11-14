from flask import Flask
from flask_jwt_extended import JWTManager
from models import db
from user_apis import user_api  # Import the Blueprint
from utility import utility

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = '5c303052273cfcb635841b9c86d4a7eef498386af15de38ff5a19bd2aeebb803'

db.init_app(app)
jwt = JWTManager(app)

# Register the api Blueprints
app.register_blueprint(user_api, url_prefix='/user') 
app.register_blueprint(utility, url_prefix='/utility') 

with app.app_context():
    db.create_all()  # Create tables if they don't exist

if __name__ == '__main__':
    app.run(debug=True)
