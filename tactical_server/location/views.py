
from flask import redirect, render_template, url_for, Blueprint, request

from .forms import LocationForm
from tactical_server.models import Soldier, Location

location_blueprint = Blueprint('location', __name__, template_folder='templates/location')

@location_blueprint.route('/list-location/<id>')
def list_location(id):
    """
    Flask Route: '/list-location/<id>'

    Function to handle requests for selecting a soldier to view the locations they have been. This function is called when the '/list-location'
    URL is accessed by the Flask app. It queries the 'location' table to retrieve all entries with the soldier_id entered by the user. It also
    queries the 'Soldier' table to get information about the soldier with the entered id. If the soldier does not exist, a 404 message is
    returned. The function then renders the 'list-location.html' template, which displays a list of all locations the soldier has been.

    Args:
    - id (int): The ID number of the soldier for whom the locations are to be viewed.

    Returns:
    - render_template: HTML page to display a list of all locations the soldier has been, along with relevant information about the soldier.
    """

    # Queries all Entries in location table with soldier_id entered by user.
    location = Location.query.filter_by(soldier_id=id).all()
    # Queries soldier using id number entered by user. Returns 404 message is entered id number does not exist in database.
    soldier = Soldier.query.get_or_404(id)
    # returns html page to display list of all locations soldier has been.
    return render_template('list-location.html', Location=location, person=soldier)


# displays locations soldier has been
@location_blueprint.route('/view-location', methods=['POST', 'GET'])
def view_location():
    """
    Flask Route: '/view-location'

    Function to handle requests for displaying the locations a soldier has been. This function is called when the '/view-location'
    URL is accessed by the Flask app. It uses the 'LocationForm' to get the soldier's ID from the user. If the form is validated upon
    submission, the function redirects to the 'list-location' route, passing the soldier's ID. This route displays a list of all
    locations the soldier has been.

    Returns:
    - render_template: HTML page containing the form to select a soldier to view their locations.
    - redirect: If the form is validated, redirects to the 'list-location' route to display the locations of the selected soldier.
    """
    form = LocationForm()  # adds form to be used in function.

    # if the form is validated when the submit button is pressed.
    if request.method == 'POST':
        id = form.id.data  # Extracts id number from data entered in form

        # Redirects to webpage to display list of soldiers locations.
        return redirect(url_for('location.list_location', id=id))
    # Returns html for form to select soldier.
    return render_template('view-location.html', form=form)
