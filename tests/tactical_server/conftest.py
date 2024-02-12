import pytest

from tactical_server import create_app
from tactical_server.database import db

@pytest.fixture()
def app():
    app = create_app('sqlite://')

    with app.app_context():
        db.create_all()

    yield app


@pytest.fixture()
def client(app):
    app.testing = True
    return app.test_client()