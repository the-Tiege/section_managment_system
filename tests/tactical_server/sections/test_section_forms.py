import datetime
import json
from tactical_server.models import Section, Soldier
from tactical_server.database import db

def test_add_section(client, app):
    response = client.post("/sections/add-section", data={"id": 1, "SectionAmmo": 5000})

    with app.app_context():
        section = Section.query.first()
        assert response.status_code == 302
        assert Section.query.count() == 1
        assert section.id == 1
        assert section.section_amunition == 5000
        assert section.section_strength == 0
        assert section.section_ok == 0
        assert section.section_casualty == 0
        assert section.section_location == "0"
        assert section.section_battery == "100"


def test_delete_section(client, app):
    
    with app.app_context():
        section = Section(1, 5000)
        db.session.add(section)
        db.session.commit()

        assert Section.query.count() == 1
        assert Section.query.first().id == 1

    response = client.post("/sections/delete-section", data={"id": 1})

    with app.app_context():
        assert response.status_code == 302
        assert Section.query.count() == 0


def test_add_amunition(client, app):
    
    with app.app_context():
        section = Section(1, 5000)
        db.session.add(section)
        db.session.commit()

        assert Section.query.count() == 1
        assert Section.query.first().section_amunition == 5000

    response = client.post("/sections/add-amunition", data={"id": 1, "SectionAmmo": 1000})

    with app.app_context():
        assert response.status_code == 302
        assert Section.query.first().section_amunition == 6000

def test_section_json(client, app):
    expected_result = [{
                        "id": 1,
                        "SectionAmmo": 5000, 
                        "SectionStrength": 0, 
                        "SectionLocation": "0",
                        "SectionOK": 0, 
                        "SectionCasualty": 0, 
                        "SectionBattery": "100"
                        }]
    
    with app.app_context():
        section = Section(1, 5000)
        db.session.add(section)
        db.session.commit()

        response = client.get("/sections/section")
        section_json = response.data.decode("utf-8")
        section_dict = json.loads(section_json)
        assert expected_result == section_dict

def test_soldier_json(client, app):
    expected_result = [{
                        "id": 1, 
                        "name": "Dunne", 
                        "role": "I/C", 
                        "Ident": "Unverified", 
                        "LastHR": 0, 
                        "currentLocation": "0",
                        "Distance": "0", 
                        "TIME": datetime.datetime.now().strftime("%I:%M"), 
                        "Rndsfired": 0, 
                        "RifleBat": "100", 
                        "State": "OK",
                        "ArmourBat": "100", 
                        "HubBattery": "100"
                        }]
    
    with app.app_context():
        section = Section(1, 5000)
        db.session.add(section)
        db.session.commit()

        soldier = Soldier(1, "Dunne", "I/C", 1)
        db.session.add(soldier)
        db.session.commit()

        response = client.get("/sections/soldiers")
        section_json = response.data.decode("utf-8")
        section_dict = json.loads(section_json)
        assert expected_result == section_dict


def test_section_overview(client, app):
    with app.app_context():
        response = client.get("/sections/section-overview")

        assert b" <h1>Section</h1>" in response.data
        assert response.status_code == 200

def test_list_section_members(client, app):
    with app.app_context():
        response = client.get("/sections/list-section-members")

        assert b"<h1>List of Section Members</h1>" in response.data
        assert response.status_code == 200


