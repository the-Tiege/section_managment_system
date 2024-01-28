import datetime  # gets date and time from computer.
import json  # used to put data into json format.
from flask import Flask, jsonify,  redirect, render_template, url_for, Blueprint, request
from forms_section.forms_section import HeartForm
    
from tactical_server.models import Soldier, Vitals

heart_rate_blueprint = Blueprint('heart_rate', __name__, template_folder='templates/heart_rate')

# display  list of soldiers heart rate to user
@heart_rate_blueprint.route('/list-heart-rate/<id>')
def list_heart_rate(id):
    """
    Flask Route: '/list-heart-rate/<id>'

    Function to handle requests for displaying a list of a soldier's heart rates. This function is called when the '/list-heart-rate'
    URL is accessed by the Flask app. It queries the database for all heart rate entries associated with the given soldier ID and also
    retrieves the soldier's information. The data is then passed to the 'list-heart-rate.html' template for rendering.

    Args:
    - id (str): Soldier ID for whom the heart rates are to be listed.

    Returns:
    - render_template: HTML page ('list-heart-rate.html') that displays the list of heart rate entries for the selected soldier.
    """

    # Queries all Entries in vitals table with soldier_id entered by user.
    Heart = Vitals.query.filter_by(soldier_id=id).all()
    # Queries soldier using id number entered by user. Returns 404 message is entered id number does not exist in database.
    person = Soldier.query.get_or_404(id)

    # Returns html page that lists vitals entries of selected soldier.
    return render_template('list-heart-rate.html', Heart=Heart, person=person)


# select which section members heart rate to view
@heart_rate_blueprint.route('/view-heart', methods=['POST', 'GET'])
def view_heart():
    """
    Flask Route: '/view-heart'

    Function to handle requests for selecting which section member's heart rate to view. This function is called when the '/view-heart'
    URL is accessed by the Flask app. It uses a form ('HeartForm') to get the ID number of the soldier for whom the heart rate entries
    need to be viewed. If the form is validated, the function redirects to the 'list-heart-rate' page for the selected soldier. Otherwise,
    it renders the 'view-heart.html' template, which includes the form for soldier selection.

    Returns:
    - redirect or render_template: If the form is validated, redirects to the 'list-heart-rate' page. Otherwise, renders 'view-heart.html'
      with the soldier selection form.
    """
    form = HeartForm()  # adds form to be used in function.

    # if the form is validated when the submit button is pressed.
    if request.method == 'POST':
        id = form.id.data  # Extracts id number from data entered in form

        # Redirects to html page to display vitals table entries for entered id number.
        return redirect(url_for('list_heart_rate', id=id))
    # Displays html page that for form to select soldier to view their vitals table entries.
    return render_template('view-heart.html', form=form)