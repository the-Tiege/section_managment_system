import datetime
from flask_sqlalchemy import SQLAlchemy
import pytest
# Replace "your_app" with the actual name of your application
from tactical_server.section_db import app, db
from tactical_server.section_db import Soldier, Vitals, Location, Section


# @pytest.fixture
# def client():
#     app.config['TESTING'] = True
#     client = app.test_client()

#     with app.app_context():
#         db.create_all()

#     yield client
def create_soldier(id, name, role, section_id):
    new_sol = Soldier(id, name, role, section_id)
    new_sol.identity_check = "Unverified"
    new_sol.last_update_time = datetime.datetime.now().strftime("%X")
    new_sol.ammunition_expended = 0
    new_sol.last_heart_rate = 0 
    new_sol.current_location = "0"
    new_sol.rifle_sensor_battery_level = "100"
    new_sol.status = "OK"
    new_sol.armour_sensor_battery_level = "100"
    new_sol.distance_traveled = "0"
    new_sol.hub_sensor_battery_level = "100"
    return new_sol

@pytest.fixture
def app_with_test_database():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_db.sqlite'  # Use an in-memory SQLite database for testing
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


    with app.app_context():
        db.create_all()

        test_soldier = create_soldier(0, "Test", "1 Scout", 1)
        db.session.add(test_soldier)
        db.session.commit()

    yield app

    with app.app_context():
        db.session.remove()
        # db.drop_all()

@pytest.fixture
def client(app_with_test_database):
    return app_with_test_database.test_client()


def test_sensor_data_database_update(client):
    # Test database updates for the '/sensor-data/<message>' route

    # Assuming your route expects the message as a string, create a message string for testing
    message_string = "id:0,HR:75,Ident:1"
    response = client.get(f'/sensor-data/{message_string}')

    assert response.status_code == 200
    assert response.data.decode('utf-8') == 'ok'

    # Check the database for updates
    with app.app_context():
        # Retrieve the updated Soldier record from the database
        updated_soldier = Soldier.query.get(0)

        # Perform assertions to check if the database is updated correctly
        assert updated_soldier.last_heart_rate == 75
        assert updated_soldier.identity_check == "Verified"
        # Add more assertions based on the expected behavior of your route

        # Check if a new entry is added to the Vitals table
        new_vital = Vitals.query.filter_by(soldier_id=0).order_by(Vitals.id.desc()).first()
        assert new_vital.heart_rate == 75
        # Add more assertions for other tables (Location, Section, etc.)

        # Clean up (optional): Delete the test records from the database
        db.session.delete(updated_soldier)
        db.session.delete(new_vital)
        db.session.commit()
