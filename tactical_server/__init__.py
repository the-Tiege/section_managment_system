from flask import Flask, render_template
from flask_migrate import Migrate

from .database import db

from tactical_server.soldiers.views import soldiers_blueprint
from tactical_server.sections.views import section_blueprint
from tactical_server.location.views import location_blueprint
from tactical_server.heart_rate.views import heart_rate_blueprint


def create_app(database_uri='sqlite:///', secret_key='mySecretKey'):
    app = Flask(__name__)

    app.config['SECRET_KEY'] = secret_key

    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    Migrate(app, db)

    app.register_blueprint(soldiers_blueprint, url_prefix='/soldiers')
    app.register_blueprint(section_blueprint, url_prefix='/sections')
    app.register_blueprint(location_blueprint, url_prefix='/location')
    app.register_blueprint(heart_rate_blueprint, url_prefix='/heart_rate')

    @app.route('/')
    def index():
        return render_template('index.html')

    return app
