
from tactical_server.models import Vitals, Soldier, Section
from tactical_server.database import db


def test_list_heart_rate(app, client):
    with app.app_context():
        section = Section(1, 5000)
        soldier = Soldier(1, "Dunne", "I/C", 1)
        heart_rate = Vitals(heart_rate=65, time="15:10:42", soldier_id=1)
        db.session.add_all([section, soldier, heart_rate])
        db.session.commit()

        response = client.get('/heart_rate/list-heart-rate/1')

        assert response.status_code == 200
        assert b'<h1>1 Dunne Heart Rate</h1>' in response.data
        assert b'<td scope="row">65</td>' in response.data
        assert b'<td>15:10:42</td>' in response.data
        
def test_view_heart_rate(app, client):
    with app.app_context():
        section = Section(1, 5000)
        soldier = Soldier(1, "Dunne", "I/C", 1)
        heart_rate = Vitals(heart_rate=65, time="15:10:42", soldier_id=1)
        db.session.add_all([section, soldier, heart_rate])
        db.session.commit()

        response = client.get('/heart_rate/view-heart')
        assert response.status_code == 200
        assert b'<h1>View Heart rate</h1>' in response.data

        response = client.post('/heart_rate/view-heart', data={'id': 1})
        assert response.status_code == 302