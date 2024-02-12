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
def test_sensor_data_location_update(client, app, id, lat, long):

    with app.app_context():
        section = Section(id, 500)
        db.session.add(section)
        
        
        soldier = Soldier(id, "Dunne", "I/C", id)
        db.session.add(soldier)
        db.session.commit()

    message_string = f"id:{id},lat:{lat},long:{long}"
    response = client.get(f'/sections/sensor-data/{message_string}')

    assert response.status_code == 200

    with app.app_context():
        new_location = Location.query.filter_by(soldier_id=id).order_by(Location.id.desc()).first()
        assert new_location.lat == lat
        assert new_location.long == long

RNDS_FIRED_Params = [
    (0, 5),
    (0, 8),
    (0, 20)
]
@pytest.mark.parametrize("id, rounds_fired", RNDS_FIRED_Params)
def test_sensor_data_rounds_fired(client, app, id, rounds_fired):

    with app.app_context():
        section = Section(id, 500)
        soldier = Soldier(id, "Dunne", "I/C", id)
        db.session.add_all([section, soldier])
        db.session.commit()

        

    message_string = f"id:{id},Rndsfired:{rounds_fired}"
    response = client.get(f'/sections/sensor-data/{message_string}')

    with app.app_context():
        updated_soldier = Soldier.query.get(id)

        assert updated_soldier.name == "Dunne"
        assert response.status_code == 200
        assert updated_soldier.ammunition_expended == rounds_fired

STATUS_PARAMS = [
    (0, 1, "Casualty"),
    (0, 0, "OK")
]
@pytest.mark.parametrize("id, status, expected_result", STATUS_PARAMS)
def test_sensor_data_status(client, app, id, status, expected_result):

    with app.app_context():
        section = Section(id, 500)
        soldier = Soldier(id, "Dunne", "I/C", id)
        db.session.add_all([section, soldier])
        db.session.commit()

    message_string = f"id:{id},State:{status}"
    response = client.get(f'/sections/sensor-data/{message_string}')

    with app.app_context():
        updated_soldier = Soldier.query.get(id)

        assert updated_soldier.name == "Dunne"
        assert response.status_code == 200
        assert updated_soldier.status == expected_result

BATTERY_LEVEL_PARAMS = [
    (0, 65, 22),
    (5, 99, 30),
    (3, 25, 32)
]       
@pytest.mark.parametrize("id, armour_bat, rifle_bat", BATTERY_LEVEL_PARAMS)
def test_sensor_data_battery_level(client, app, id, armour_bat, rifle_bat):

    with app.app_context():
        section = Section(id, 500)
        soldier = Soldier(id, "Dunne", "I/C", id)
        db.session.add_all([section, soldier])
        db.session.commit()

    message_string = f"id:{id},ArmourBat:{armour_bat},RifleBat:{rifle_bat}"
    response = client.get(f'/sections/sensor-data/{message_string}')

    with app.app_context():
        updated_soldier = Soldier.query.get(id)

        assert updated_soldier.name == "Dunne"
        assert response.status_code == 200
        assert updated_soldier.rifle_sensor_battery_level == str(rifle_bat)
        assert updated_soldier.armour_sensor_battery_level == str(armour_bat)
        
IDENTITY_CHECK_PARAMS = [
    (0, 1, "Verified"),
    (0, 0, "Unverified")
]
@pytest.mark.parametrize("id, identity_check, expected_result", IDENTITY_CHECK_PARAMS)
def test_sensor_data_identity_check(client, app, id, identity_check, expected_result):

    with app.app_context():
        section = Section(id, 500)
        soldier = Soldier(id, "Dunne", "I/C", id)
        db.session.add_all([section, soldier])
        db.session.commit()

    message_string = f"id:{id},Ident:{identity_check}"
    response = client.get(f'/sections/sensor-data/{message_string}')

    with app.app_context():
        updated_soldier = Soldier.query.get(id)

        assert updated_soldier.name == "Dunne"
        assert response.status_code == 200
        assert updated_soldier.identity_check == expected_result