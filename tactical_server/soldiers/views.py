import datetime

from flask import redirect, render_template, url_for, Blueprint, request

from .forms import AddForm, DelForm 
from tactical_server.database import db
from tactical_server.models import Soldier, Section

soldiers_blueprint = Blueprint('soldiers', __name__, template_folder='templates/soldiers')

# add person to section,uses army number as primary key to add member to section. initial values automatically given.
@soldiers_blueprint.route('/add-soldier', methods=['GET', 'POST'])
def add_soldier():
    """
    Flask Route: '/add-soldier'

    Function to handle requests for adding a new soldier to a section. This function is called when the '/add-soldier' URL is accessed
    by the Flask app. The function processes the form data submitted, creates a new soldier entry, and updates the section
    information accordingly.

    Returns:
    - str or redirect: If the form is successfully validated and the soldier is added, it redirects to the 'list' page. If not,
      it returns the HTML page ('add-soldier.html') for adding a new member to the section.
    """
    form = AddForm()  # adds form to be used in function.

    # if the form is validated when the submit button is pressed.
    if request.method == 'POST':

        id = form.id.data  # Extracts id number from data entered in form
        # Extracts Soldiers name from data entered in form.
        name = form.name.data
        # Extracts Soldiers role from data entered in form.
        role = form.role.data
        # Extracts Soldiers Section id from data entered in form.
        section_id = form.section_id.data

        # Creates new soldier using data entered in form.
        new_sol = Soldier(id, name, role, section_id)
        # Sets initial for Identity verification.
        new_sol.identity_check = "Unverified"
        # Sets initial for time using time extracted from computer clock.
        new_sol.last_update_time = datetime.datetime.now().strftime("%X")
        # Sets initial value for ammunition fired by soldier to 0.
        new_sol.ammunition_expended = 0
        new_sol.last_heart_rate = 0  # Sets initial value for heart rate to 0.
        new_sol.current_location = "0"  # Sets initial value for location TO 0.
        # Sets initial value for rifle battery to 100.
        new_sol.rifle_sensor_battery_level = "100"
        new_sol.status = "OK"  # Sets initial value for State to "OK".
        # Sets initial value for Armour battery to 100.
        new_sol.armour_sensor_battery_level = "100"
        # Sets initial values for Distance traveled to 0.
        new_sol.distance_traveled = "0"
        # Sets initial value for HubBattery to 100.
        new_sol.hub_sensor_battery_level = "100"
        db.session.add(new_sol)  # adds soldier to database.
        db.session.commit()  # Saves change to database.

        # Queries Section table using section id of soldier.
        update_section = Section.query.get(section_id)
        # Adds one to section Strength for new person added to section.
        update_section.section_strength = update_section.section_strength + 1
        # Adds one person to SectionOK for new person added to section.
        update_section.section_ok = update_section.section_ok + 1
        db.session.add(update_section)  # Adds updated information to database.
        db.session.commit()  # Saves change to database.

        # Redirects to html page that displays List of section members.
        return redirect(url_for('list_section_members'))

    # returns html page for form to add member to section.
    return render_template('add-soldier.html', form=form)

# remove soldier from section
@soldiers_blueprint.route('/delete-soldier', methods=['POST', 'GET'])
def delete_soldier():
    """
    Flask Route: '/delete-soldier'

    Function to handle requests for removing a soldier from a section. This function is called when the '/delete-soldier' URL
    is accessed by the Flask app using the POST or GET method. It uses a form to get the soldier's ID, queries the
    Soldier table using the ID, deletes the soldier's entry from the database, and updates the section information
    accordingly.

    Returns:
    - redirect: Redirects to the '/list' URL to display the updated section information.

    HTML Template:
    - 'delete-soldier.html': Returns HTML page for the form to delete a section member if the form is not validated.
    """
    form = DelForm()  # adds form to be used in function.

    # if the form is validated when the submit button is pressed.
    if request.method == 'POST':
        id = form.id.data  # Extracts id number from data entered in form
        # Queries Soldiers table using entered id returns 404 message id query does not exist.
        soldier = Soldier.query.get_or_404(id)
        db.session.delete(soldier)  # Deletes entry from database.
        db.session.commit()  # Saves change to database.

        # Queries Section table using section id of soldier.
        update_section = Section.query.get(soldier.section_id)
        # Takes one from section Strength for person removed from section.
        update_section.section_strength -= 1
        # Takes one from section Ok for person removed from section..
        update_section.section_ok -= 1
        db.session.add(update_section)  # Adds updated information to database.
        db.session.commit()  # Saves change to database.

        # Redirects to page to display section information.
        return redirect(url_for('list_section_members'))
    # Returns html page for form to delete section member.
    return render_template('delete-soldier.html', form=form)
