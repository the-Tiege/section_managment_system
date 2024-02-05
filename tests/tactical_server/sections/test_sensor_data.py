import pytest
from tactical_server.database import db
from tactical_server.models import Soldier, Vitals, Location, Section

HR_Params = [
    (0, 75),
    (0, 88),
    (0, 55)
]

@pytest.mark.parametrize("id, heart_rate", HR_Params)
def test_sensor_data_heart_rate_update(client, app, id, heart_rate):

    with app.app_context():
        section = Section(id, 500)
        db.session.add(section)
        
        
        soldier = Soldier(id, "Dunne", "I/C", id)
        db.session.add(soldier)
        db.session.commit()

        

    message_string = f"id:{id},HR:{heart_rate}"
    response = client.get(f'/sections/sensor-data/{message_string}')

    with app.app_context():
        updated_soldier = Soldier.query.get(id)

        assert updated_soldier.name == "Dunne"
        assert response.status_code == 200
        assert updated_soldier.last_heart_rate == heart_rate
        new_vital = Vitals.query.filter_by(soldier_id=id).order_by(Vitals.id.desc()).first()
        assert new_vital.heart_rate == heart_rate
        


LOCATION_Params = [
    (0, "52.65913", "-8.62513"),
    (0, "52.6540", "-8.62994"),
    (0, "52.66206", "-8.20898")
]

@pytest.mark.parametrize("id, lat, long", LOCATION_Params)
def test_sensor_data_loction_update(client, app, id, lat, long):

    with app.app_context():
        section = Section(id, 500)
        db.session.add(section)
        
        
        soldier = Soldier(id, "Dunne", "I/C", id)
        db.session.add(soldier)
        db.session.commit()

    message_string = f"id:{id},lat:{lat},long:{long}"
    response = client.get(f'/sections/sensor-data/{message_string}')

    assert response.status_code == 200

    # Check the database for updates
    with app.app_context():
        new_location = Location.query.filter_by(soldier_id=id).order_by(Location.id.desc()).first()
        assert new_location.lat == lat
        assert new_location.long == long
        