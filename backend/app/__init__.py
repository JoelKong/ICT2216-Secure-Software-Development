from flask import Flask
from flask_cors import CORS
from .db import db
from .routes.auth import auth_bp
import os

# Initialise app
def create_app():
    app = Flask(__name__)
    #TODO: dk if need secure this and need adjust origin for cloud
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})
    
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config["SECRET_KEY"] = os.getenv('SECRET_KEY', 'defaultsecretkey') #TODO: gpt say this is for session? idk
    db.init_app(app)

    app.register_blueprint(auth_bp, url_prefix='/api')

    return app
