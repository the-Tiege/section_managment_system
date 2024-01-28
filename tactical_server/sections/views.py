from flask import redirect, render_template, url_for, Blueprint
from forms_section.forms_section import Addammo, CreateSection, DelSection

from tactical_server.database import db
from tactical_server.models import Section, Soldier

section_blueprint = Blueprint('sections', __name__, template_folder='templates/sections')
    




@section_blueprint.route('/add-section', methods=['GET', 'POST'])
def add_section():
    """
    Flask Route: '/add-section' (GET and POST)

    Function to handle requests for adding a new section. This function is called when the '/add-section' URL is
    accessed by the Flask app, and it supports both GET and POST methods. It uses the 'CreateSection' form to gather
    user input.

    If the form is validated on submission, it extracts the section's ID and ammunition from the form, creates a new
    section with default values, and adds it to the database. Then, it redirects to the 'section-overview' page.

    Returns:
    - str: Rendered HTML page ('add-section.html') with the 'CreateSection' form for creating a new section.
            Or, redirects to the 'section-overview' page if a new section is successfully added.
    """
    form = CreateSection()  # adds CreateSection form to be used in function.

    # if the form is validated when the submit button is pressed.
    if form.validate_on_submit():

        id = form.id.data  # Extracts id number from data entered in form.
        # Extracts Ammunition from data entered in form.
        SectionAmmo = form.SectionAmmo.data

        # Creates new section member form data entered in form.
        new_sec = Section(id, SectionAmmo)
        # Sets initial value of section strength to 0.
        new_sec.section_strength = 0
        new_sec.section_ok = 0  # Sets initial value of SectionOK to 0.
        # Sets initial value of Casualties in section to 0.
        new_sec.section_casualty = 0
        new_sec.section_location = "0"  # Sets initial value of location to 0.
        # Sets initial value of Battery to to 100.
        new_sec.section_battery = "100"
        # Takes object created from data taken from form and adds it to database.
        db.session.add(new_sec)
        db.session.commit()  # Saves change made to database.

        # Redirects to page that displays Section information.
        return redirect(url_for('section_overview'))

    # Returns Html page for form to create a new section.
    return render_template('add-section.html', form=form)


# function to add a section
@section_blueprint.route('/add-amunition', methods=['GET', 'POST'])
def add_ammo():
    """
    Flask Route: '/add-amunition' (GET and POST)

    Function to handle requests for adding ammunition to a section. This function is called when the '/add-amunition'
    URL is accessed by the Flask app, and it supports both GET and POST methods. It uses the 'Addammo' form to gather
    user input.

    If the form is validated on submission, it extracts the section's ID and ammunition from the form, queries the
    database to get the corresponding section, adds the ammunition to the section, and updates the database. Then, it
    redirects to the 'section-overview' page.

    Returns:
    - str: Rendered HTML page ('add-amunition.html') with the 'Addammo' form for adding ammunition to a section.
            Or, redirects to the 'section-overview' page if ammunition is successfully added to the section.
    """
    form = Addammo()  # adds form to be used in function.

    # if the form is validated when the submit button is pressed.
    if form.validate_on_submit():

        id = form.id.data  # Extracts id number from data entered in form
        # Extracts ammunition from data enter in form.
        amuntion_added = form.SectionAmmo.data

        # Queries database using entered id number returns 404 message if number entered is not in database.
        resupply = Section.query.get_or_404(id)
        # Takes ammunition added in form and adds it to section ammunition.
        resupply.section_amunition += amuntion_added
        db.session.add(resupply)  # Adds new entry to database.
        db.session.commit()  # Saves change to database.

        # redirects to page that displays section information.
        return redirect(url_for('section_overview'))

    # returns html page that displays page to add ammunition to section.
    return render_template('add-amunition.html', form=form)


@section_blueprint.route('/section-overview')  # Displays section overview to user
def section_overview():
    """
    Flask Route: '/section-overview'

    Function to handle requests for displaying the section overview to the user. This function is called when the
    '/section-overview' URL is accessed by the Flask app.

    Returns:
    - str: Rendered HTML page ('section-overview.html') containing the overview of the section.
    """

    # Returns html page for overview of section.
    return render_template('section-overview.html')


@section_blueprint.route('/delete-section', methods=['POST', 'GET'])  # Remove section
def delete_section():
    """
    Route handler to remove a section along with its associated soldiers.

    This function handles HTTP GET and POST requests for deleting a section. If the provided form is validated,
    it extracts the section ID and deletes all soldiers associated with that section. Finally, it deletes the
    specified section from the database.

    Parameters:
    - None

    Returns:
    - GET Request: Renders the 'delete-section.html' template with the deletion form.
    - POST Request: Redirects to the 'section-overview' route after successfully deleting the section and associated soldiers.
    """

    form = DelSection()  # adds form to be used in function.

    # if the form is validated when the submit button is pressed.
    if form.validate_on_submit():
        id = form.id.data  # Extracts id number from data entered in form
        # When section is deleted. Queries all soldiers with same section id and deletes them.
        soldiers = Soldier.query.filter_by(section_id=id).all()

        for i in soldiers:  # for loop to iterate through soldiers returned by query.
            db.session.delete(i)  # deletes soldier.
            db.session.commit()  # saves change to database.

        # Queries section using entered id data taken from form. Returns 404 message if no entry exists.
        section = Section.query.get_or_404(id)
        db.session.delete(section)  # Deletes section.
        db.session.commit()  # Saves change to database.
        # redirects to page that displays section information.
        return redirect(url_for('section_overview'))

    # Returns html page of form to delete section.
    return render_template('delete-section.html', form=form)