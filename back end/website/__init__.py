from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"
DB_PATH = os.path.join(os.path.dirname(__file__), DB_NAME)

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'Navabeghe Sharif'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
    db.init_app(app)

    create_database(app)
    return app

def create_database(app):
    if not os.path.exists('website/database.db'):
        with app.app_context():
            db.create_all()
        print('Database created!')