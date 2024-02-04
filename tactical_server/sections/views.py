from flask import redirect, render_template, url_for, Blueprint, request
from .forms import Addammo, CreateSection, DelSection

import json
import datetime

from tactical_server.database import db
from tactical_server.models import Section, Soldier, Vitals, Location

from .convert_to_dict import convert_to_dict
from geopy import distance
from .lat_long_to_grid_reference import lat_long_to_grid_reference

section_blueprint = Blueprint(
    'sections', __name__, template_folder='templates/sections')


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
    # if form.validate_on_submit():
    if request.method == "POST":

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
        return redirect(url_for('sections.section_overview'))

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
        return redirect(url_for('sections.section_overview'))

    # returns html page that displays page to add ammunition to section.
    return render_template('add-amunition.html', form=form)


# Displays section overview to user
@section_blueprint.route('/section-overview')
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


# Remove section
@section_blueprint.route('/delete-section', methods=['POST', 'GET'])
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
        return redirect(url_for('sections.section_overview'))

    # Returns html page of form to delete section.
    return render_template('delete-section.html', form=form)


# list all members in section
@section_blueprint.route('/list-section-members')
def list_section_members():
    """
    Flask Route: '/list-section-members'

    Function to handle requests for listing all members in a section. This function is called when the '/list-section-members' URL is accessed
    by the Flask app. It returns an HTML page ('list-section-members.html') that displays a list of soldiers in the section.

    Returns:
    - render_template: HTML page for displaying the list of soldiers in the section.
    """

    # Returns html page that that displays soldiers in section.
    return render_template('list-section-members.html')

# sends section information to a page in json script format.


@section_blueprint.route('/section', methods=['GET'])
def section_json_information():
    """
    Flask Route: '/section'

    Function to handle requests for section information in JSON script format. This function is called when the '/section'
    URL is accessed by the Flask app using the GET method. It queries all section information from the database, formats it
    into a list of dictionaries, each representing a section, and returns the result as a JSON script.

    Returns:
    - str: JSON script containing section information, formatted as a list of dictionaries.
    """

    section = Section.query.all()  # Queries all section information.

    sections = []  # blank list to store json information.
    # For loop to iterate through Queried data and store it in a list printed in json format.
    for i in section:
        soldier = {"id": i.id, "SectionAmmo": i.section_amunition, "SectionStrength": i.section_strength, "SectionLocation": i.section_location,
                   "SectionOK": i.section_ok, "SectionCasualty": i.section_casualty, "SectionBattery": i.section_battery}  # Queried information printed as json.
        sections.append(soldier)  # information appended to list.

    # print(json.dumps(sections))
    # list converted to json and printed to page'/section'
    return json.dumps(sections)


# sends section information to a page in json script format.
@section_blueprint.route('/soldiers', methods=['GET'])
def soldier_json_information():
    """
    Flask Route: '/soldiers'

    Function to handle requests for soldier information in JSON script format. This function is called when the '/soldiers'
    URL is accessed by the Flask app using the GET method. It queries all soldier information from the database, formats it
    into a list of dictionaries, each representing a soldier, and returns the result as a JSON script.

    Returns:
    - str: JSON script containing soldier information, formatted as a list of dictionaries.
    """

    section = Soldier.query.all()  # Queries all Soldier information.

    sections = []  # blank list to store json information.
    # For loop to iterate through Queried data and store it in a list printed in json format.
    for i in section:
        soldier = {"id": i.id, "name": i.name, "role": i.role, "Ident": i.identity_check, "LastHR": i.last_heart_rate, "currentLocation": i.current_location,
                   "Distance": i.distance_traveled, "TIME": i.last_update_time, "Rndsfired": i.ammunition_expended, "RifleBat": i.rifle_sensor_battery_level, "State": i.status,
                   "ArmourBat": i.armour_sensor_battery_level, "HubBattery": i.hub_sensor_battery_level}  # Queried information printed as json.
        sections.append(soldier)  # information appended to list.

    # print(json.dumps(sections))
    # list converted to json and printed to page'/section'
    return json.dumps(sections)


@section_blueprint.route('/sensor-data/<message>')
def sensor_data(message):
    """
    Flask Route: '/sensor-data/<message>'

    Function to handle requests for updating the database with information sent by Arduino. This function is called when
    the '/sensor-data/<message>' URL is accessed by the Flask app. The Arduino sends data, which is converted into a dictionary
    using the 'Convert' function. The function then updates the Soldier table in the database based on the received data,
    including time, identity verification, heart rate, location, distance traveled, ammunition fired, rifle battery,
    body armor state, and body armor battery.

    Args:
    - message (str): Information sent by Arduino.

    Returns:
    - str: Returns "ok" as a message to the Arduino indicating that the update was successful.

    Database Updates:
    - Soldier table: Updates soldier's information based on the received data.
    - Vitals table: Creates a new entry with heart rate information.
    - Location table: Creates a new entry with location information.
    - Section table: Updates section information based on the soldier's role, casualties, and ammunition fired.

    Note:
    - The function assumes the existence of the 'Convert' function, which is not provided in the code snippet.

    Examples:
    - Accessing '/sensor-data/123456?HR=80&Ident=1&long=40.7128&lat=-74.0060&TIME=12:00&Rndsfired=5&RifleBat=80&State=1&ArmourBat=90'
      would update the database for the soldier with ID 123456 based on the provided data.
    """

    # calls function to convert data sent from arduino to dictionary.
    message_dict = convert_to_dict(message)

    # Queries database for using id number stored in dictionary.
    update_db = Soldier.query.get(message_dict['id'])

    # Updates time of last entry using computer clock.
    update_db.last_update_time = datetime.datetime.now().strftime("%X")
    db.session.add(update_db)  # Stores update to database.
    db.session.commit()  # Saves change to database.

    if 'Ident' in message_dict:  # Checks dict for Identity check.
        # if arduino sends 1 identity is verified.
        if message_dict['Ident'] == "1":
            # Updates identity as verified.
            update_db.identity_check = "Verified"
            db.session.add(update_db)  # Stores update to database.
            db.session.commit()  # Saves change to database.
        else:
            # Updates identity as unverified.
            update_db.identity_check = "Unverified"
            db.session.add(update_db)  # Stores update to database.
            db.session.commit()  # Saves change to database.

    if 'HR' in message_dict:  # Checks dict for heart rate
        # Updates database using information in dictionary
        update_db.last_heart_rate = message_dict['HR']
        db.session.add(update_db)  # Stores update to database.
        db.session.commit()  # Saves change to database.

        # Creates new entry in vitals table using data received from arduino and time from computer clock.
        new_vital = Vitals(message_dict['HR'], datetime.datetime.now().strftime(
            "%X"), message_dict['id'])
        db.session.add(new_vital)  # Stores update to database.
        db.session.commit()  # Saves change to database.

    # Checks dict for latitude and longitude.
    if 'long' in message_dict and 'lat' in message_dict:
        update_db.current_location = lat_long_to_grid_reference(float(message_dict['lat']), float(
            message_dict['long']))  # converts lat and long to grid reference.
        db.session.add(update_db)  # Stores update to database.
        db.session.commit()  # Saves change to database.

        # Creates new entry in location table using data received from arduino and time from computer clock.
        new_location = Location(message_dict['long'], message_dict['lat'], lat_long_to_grid_reference(float(
            message_dict['lat']), float(message_dict['long'])), datetime.datetime.now().strftime("%X"), message_dict['id'])
        db.session.add(new_location)  # Stores update to database.
        db.session.commit()  # Saves change to database.

        # If the role of the soldier is the section I/C then their location is used for section location.
        if update_db.role == "I/C":
            # queries Section table using Section ID of soldier.
            update_section = Section.query.get(update_db.section_id)
            # Sets section location to Section commanders current location.
            update_section.section_location = update_db.current_location
            db.session.add(update_section)  # Stores update to database.
            db.session.commit()  # Saves change to database.

        # Queries table of locations using Id number of soldier and returns all entries.
        Traveled = Location.query.filter_by(
            soldier_id=message_dict['id']).all()
        # If there is more that one entry for location gets the distance between those locations.
        if len(Traveled) > 1:
            dist = 0  # Stores distance traveled.
            i = 0  # used to increment through array in while loop.
            # increments through list of locations getting the distance between two points at each increment.
            while i < len(Traveled):
                # breaks from loop on second last entry otherwise an error is caused.
                if i == (len(Traveled)-1):
                    break
                else:  # adds distance between the two points currently being calculated and adds them to total distance.
                    # Function distance.distance() taken from package geopy. Takes two latitude longitude points as an argument,
                    # returns the distance between those two points, the .m at the end of the function has selected the returned value to be in meters.
                    dist = dist + distance.distance([float(Traveled[i].lat), float(Traveled[i].long)], [
                                                    float(Traveled[i+1].lat), float(Traveled[i+1].long)]).m
                i = i + 1  # used to increment through list.
            if dist > 1000:  # if the distance in meters is greater than 1000 converts to Km
                # round() function used to keep answer to 3 decimal places.
                dist = str(round(dist/1000.0, 3)) + "Km"
            else:
                dist = str(round(dist, 3)) + "m"

            # Queries database using soldiers Id
            updateDistance = Soldier.query.get(message_dict['id'])
            # updates distance traveled.
            updateDistance.distance_traveled = dist
            db.session.add(updateDistance)  # Stors update to database.
            db.session.commit()  # Saves change to database.

        # This was used when I would get the time of an update from the GPS RTC.
    if 'TIME' in message_dict:  # Checks dict for TIME
        # Updates database using information in dictionary
        update_db.last_update_time = message_dict['TIME']
        db.session.add(update_db)  # Stores update to database.
        db.session.commit()  # Saves change to database.

    if 'Rndsfired' in message_dict:  # Checks dict for ammunition fired
        update_db.ammunition_expended = update_db.ammunition_expended + \
            message_dict['Rndsfired']  # Updates database using information in dictionary
        db.session.add(update_db)  # Stores update to database.
        db.session.commit()  # Saves change to database.

        # Queries Section table using section id of soldier.
        update_section_ammo = Section.query.get(update_db.section_id)
        # updates total of ammunition left in the section base on rounds fired by th soldier.
        update_section_ammo.section_amunition = update_section_ammo.section_amunition - \
            message_dict['Rndsfired']
        db.session.add(update_section_ammo)  # Stores update to database.
        db.session.commit()  # Saves change to database.

    if 'RifleBat' in message_dict:  # Checks dict for Rifle battery information.
        # Updates database using information in dictionary
        update_db.rifle_sensor_battery_level = message_dict['RifleBat']
        db.session.add(update_db)  # Stores update to database.
        db.session.commit()  # Saves change to database.

    if 'State' in message_dict:  # Checks dict for if body armour sensor was triggered.
        # If 'State' is set to '1' sensor has been triggered.
        if message_dict['State'] == "1":
            # changes value in 'State' to 'Casualty'.
            update_db.status = "Casualty"
            db.session.add(update_db)  # Stores update to database.
            db.session.commit()  # Saves change to database.

            # Queries Section table using section id of soldier.
            SectionCas = Section.query.get(update_db.section_id)
            # Adds 1 to Casualty in section table.
            SectionCas.section_casualty = SectionCas.section_casualty + 1
            # Removes 1 from section ok.
            SectionCas.section_ok = SectionCas.section_ok - 1
            db.session.add(SectionCas)  # Stores update to database.
            db.session.commit()  # Saves change to database.

        else:
            update_db.status = "OK"  # State is OK
            db.session.add(update_db)  # Stores update to database.
            db.session.commit()  # Saves change to database.

    if 'ArmourBat' in message_dict:  # Checks dict for Body armour battery level.
        # Updates database using information in dictionary
        update_db.armour_sensor_battery_level = message_dict['ArmourBat']
        db.session.add(update_db)  # Stores update to database.
        db.session.commit()  # Saves change to database.

    return "ok"  # message returned to arduino by server.
