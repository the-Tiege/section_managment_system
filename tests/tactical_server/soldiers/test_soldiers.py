from tactical_server.models import Soldier, Section
from tactical_server.database import db

def test_add_soldier(client, app):
    client.post('/sections/add-section', data={'id': 1, 'SectionAmmo': 5000})
    
    response = client.post('/soldiers/add-soldier', data={'id': 1, 'name': "Dunne", 'section_id': '1', 'role': '3 Rifleman'})

    with app.app_context():
        soldier = Soldier.query.first()
        assert response.status_code == 302
        assert Soldier.query.count() == 1
        assert soldier.name == "Dunne"
        assert soldier.id == 1
        assert soldier.section_id == 1
        assert soldier.role == "3 Rifleman"

def test_delete_soldier(client, app):
    client.post('/sections/add-section', data={'id': 1, 'SectionAmmo': 5000})
    client.post('/soldiers/add-soldier', data={'id': 1, 'name': "Dunne", 'section_id': '1', 'role': '3 Rifleman'})

    response = client.post('/soldiers/delete-soldier', data={'id': 1})

    with app.app_context():
        assert response.status_code == 302
        assert Soldier.query.count() == 0