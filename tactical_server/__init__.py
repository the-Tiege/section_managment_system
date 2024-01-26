from flask import Flask
from flask_migrate import Migrate 

from .extensions import db
from .models import Soldier, Vitals, Location, Section
from .routes import main

def create_app(database_uri='sqlite:///', secret_key='mySecretKey'):
    app = Flask(__name__)

    app.config['SECRET_KEY'] = secret_key

    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    Migrate(app, db) 
    
    app.register_blueprint(main)

    return app
