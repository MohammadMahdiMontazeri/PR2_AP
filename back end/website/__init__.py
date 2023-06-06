from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()
DB_NAME = "database.db"
DB_PATH = os.path.join(os.path.dirname(__file__), DB_NAME)

TEMPLATE_ROOT = os.path.join(os.path.dirname(__file__), '../../front end')
STATIC_ROOT = os.path.join(os.path.dirname(__file__), '../../front end')

def create_app():
    app = Flask(__name__, template_folder=TEMPLATE_ROOT, static_folder=STATIC_ROOT, static_url_path='/')
    app.config['SECRET_KEY'] = 'Navabeghe Sharif'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
    db.init_app(app)

    from .views import views

    app.register_blueprint(views, url_prefix='/')

    from .models import Cart, Products

    create_database(app)
    return app

def create_database(app):
    if not os.path.exists('website/database.db'):
        with app.app_context():
            db.create_all()
        print('Database created!')