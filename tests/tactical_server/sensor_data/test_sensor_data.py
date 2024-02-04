import datetime
import pytest
# Replace "your_app" with the actual name of your application
from tactical_server.database import db
from tactical_server.models import Soldier, Vitals, Location, Section
from tactical_server import create_app


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

def remove_soldier(id):
    soldier = Soldier.query.get_or_404(id)
    db.session.delete(soldier) 
    db.session.commit() 

    update_section = Section.query.get(soldier.section_id)
    update_section.section_strength -= 1
    update_section.section_ok -= 1
    db.session.add(update_section)
    db.session.commit()

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

@pytest.fixture
def client(app_with_test_database):
    return app_with_test_database.test_client()

HR_Params = [
    (0, 75),
    (0, 88),
    (0, 55)
]

@pytest.mark.parametrize("id, heart_rate", HR_Params)
def test_sensor_data_heart_rate_update(client, id, heart_rate):

    message_string = f"id:{id},HR:{heart_rate}"
    response = client.get(f'/sensor-data/{message_string}')

    assert response.status_code == 200
    assert response.data.decode('utf-8') == 'ok'

    # Check the database for updates
    with app.app_context():

        # Retrieve the updated Soldier record from the database
        updated_soldier = Soldier.query.get(id)
        try:
            # Perform assertions to check if the database is updated correctly
            assert updated_soldier.last_heart_rate == heart_rate

            # Check if a new entry is added to the Vitals table
            new_vital = Vitals.query.filter_by(soldier_id=id).order_by(Vitals.id.desc()).first()
            assert new_vital.heart_rate == heart_rate
        finally:
            # Clean up (optional): Delete the test records from the database
            db.session.delete(updated_soldier)
            db.session.delete(new_vital)
            db.session.commit()


LOCATION_Params = [
    (0, "52.65913", "-8.62513"),
    (0, "52.6540", "-8.62994"),
    (0, "52.66206", "-8.20898")
]

@pytest.mark.parametrize("id, lat, long", LOCATION_Params)
def test_sensor_data_loction_update(client, id, lat, long):

    message_string = f"id:{id},lat:{lat},long:{long}"
    response = client.get(f'/sensor-data/{message_string}')

    assert response.status_code == 200
    assert response.data.decode('utf-8') == 'ok'

    # Check the database for updates
    with app.app_context():

        # Retrieve the updated Soldier record from the database
        updated_soldier = Soldier.query.get(id)

        # Update Test for current location
        # Perform assertions to check if the database is updated correctly
        # assert updated_soldier.current_location.lat == lat
        # assert updated_soldier.current_location.long == long

        # Check if a new entry is added to the Vitals table
        new_location = Location.query.filter_by(soldier_id=id).order_by(Location.id.desc()).first()
        try:
            assert new_location.lat == lat
            assert new_location.long == long
        finally:
            # Clean up (optional): Delete the test records from the database
            db.session.delete(updated_soldier)
            db.session.delete(new_location)
            db.session.commit()