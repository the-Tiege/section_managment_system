
from tactical_server.models import Location, Soldier, Section
from tactical_server.database import db


def test_list_location(app, client):
    with app.app_context():
        section = Section(1, 5000)
        soldier = Soldier(1, "Dunne", "I/C", 1)
        location = Location(lat="52.65913", long="-8.62513", grid="R5775456590", soldier_id=1, time="15:10:42")
        db.session.add_all([section, soldier, location])
        db.session.commit()

        response = client.get('/location/list-location/1')

        assert response.status_code == 200
        assert b'<h1>1 Dunne Location</h1>' in response.data
        assert b'<td scope="row">52.65913</td>' in response.data
        assert b'<td>-8.62513</td>' in response.data
        assert b'<td>R5775456590</td>' in response.data
        assert b'<td>15:10:42</td>' in response.data
        
def test_view_location(app, client):
    with app.app_context():
        section = Section(1, 5000)
        soldier = Soldier(1, "Dunne", "I/C", 1)
        location = Location(lat="52.65913", long="-8.62513", grid="R5775456590", soldier_id=1, time="15:10:42")
        db.session.add_all([section, soldier, location])
        db.session.commit()

        response = client.get('/location/view-location')
        assert response.status_code == 200
        assert b'<h1>View Location</h1>' in response.data

        response = client.post('/location/view-location', data={'id': 1})
        assert response.status_code == 302