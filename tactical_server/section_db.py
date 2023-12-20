#######################Imports######################################
import os#package used to get file path.
import json#used to put data into json format.
from json import dumps#used to put data into json format.
import datetime#gets date and time from computer.
from Dict_convert import Convert#function to handle data sent from arduino.
from LatLong_to_OS import OS_GRID#converts lat and long to grid reference.
from geopy import distance#function used to get distance between two gps locations.
from Forms_section import AddForm, DelForm, CreateSection, DelSection, HeartForm, LocationForm, Addammo#forms to take input from user.
from flask import Flask,render_template,url_for,redirect, jsonify#functions imported from flask package.
from flask_sqlalchemy import SQLAlchemy#package used to handle data base.
from flask_migrate import Migrate#used to manage changes to database.

app = Flask(__name__)#creates flask app.

app.config['SECRET_KEY'] = 'mySecretKey'#used for encryption.


##########Make SQL File##################

basdir = os.path.abspath(os.path.dirname(__file__))#gets path to current file.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basdir,'section_db.sqlite')#creates sqlite database in same folder.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False#turn off modification tracking.

db = SQLAlchemy(app)#create Sqlalchemy app.
Migrate(app,db)#create migration object.

##########Tables#########################

class Section(db.Model):
    """
    Represents a section within the system, tracking various attributes and states.

    This class corresponds to the 'Section' table in the database.

    Attributes:
        id (int): Identifying number of the section, serving as the primary key.
        section_amunition (int): Total ammunition available in the section.
        section_strength (int): Number of personnel in the section.
        section_ok (int): Number of uninjured soldiers in the section.
        section_casualty (int): Number of soldiers in the section who have become casualties.
        section_location (str): Location of the section, obtained from the section commander.
        section_battery (str): Battery level indication for the section database.
        Soldier (relationship): One-to-many relationship to the 'Soldier' table.

    Methods:
        __init__(self, id, section_ammo):
            Initializes a new Section instance.
            
            Args:
                id (int): Identifying number of the section, must be unique.
                section_ammo (int): Starting ammunition for the section.
    """

    __tablename__ = 'sections'#name of the table.

    id = db.Column(db.Integer, primary_key=True)#section number used as primary key.
    section_amunition = db.Column(db.Integer)#total ammunition in the section.
    section_strength = db.Column(db.Integer)#Number of people in the section.
    section_ok = db.Column(db.Integer)#Soldiers in section who are uninjured.
    section_casualty = db.Column(db.Integer)#Soldiers in section who have become casualties.
    section_location = db.Column(db.Text)#Location of section, Taken from section commanders location.
    section_battery = db.Column(db.Text)#battery level indication for Section database.
    soldiers = db.relationship('Soldier', backref='sections', lazy='dynamic')#relationship to table soldiers.

    def __init__(self,id,section_ammo):
        """
        Initializes a new section.

        To create the section, it requires an entry of an id number and ammunition.

        Args:
            id (int): Identifying number of the section, must be unique.
            section_ammo (int): Sections starting ammunition.
        """
        self.id = id#Identifying number of the section must be unique.
        self.section_amunition = section_ammo#Sections starting ammunition.


class Soldier(db.Model):
    """
    Represents an individual soldier within the system, providing detailed information about each soldier.

    This class corresponds to the 'soldiers' table in the database.

    Attributes:
        id (int): Army number of the soldier, serving as the primary key. Must be unique.
        name (str): Soldier's name.
        role (str): Role of the section member.
        section_id (int): ID number of the section that the soldier belongs to.
        identity_check (str): Used to verify the soldier's identity.
        vitals (relationship): One-to-many relationship to the 'vitals' table, listing the soldier's heart rate over time.
        location_history (relationship): One-to-many relationship to the 'location' table, listing the soldier's location over time.
        current_location (str): Stores the current location of the soldier.
        last_heart_rate (int): Stores the most recent record of the soldier's heart rate.
        last_update_time (str): Stores the time of the last update.
        ammunition_expended (int): Stores the number of rounds fired by the soldier.
        rifle_sensor_battery_level (str): Stores the battery level of the ammunition tracker.
        status (str): Stores the status of the soldier.
        armour_sensor_battery_level (str): Stores the battery level of the body armour sensor.
        hub_sensor_battery_level (str): Stores the battery level of the sensor hub.
        distance_traveled (str): Stores the distance traveled by the soldier.

    Methods:
        __init__(self, id, name, role, section_id):
            Initializes a new Soldier instance.
            
            Args:
                id (int): Army number, must be unique.
                name (str): Soldier's name.
                role (str): Soldier's role in the section.
                section_id (int): Section ID to which the soldier belongs.
    """

    __tablename__='soldiers'#Table name.

    id = db.Column(db.Integer,primary_key=True)#Army number  of soldier primary key. Must be unique.
    name = db.Column(db.Text)#Soldiers name.
    role = db.Column(db.Text)#Role of section member.
    section_id = db.Column(db.Integer,db.ForeignKey('sections.id'))#ID number of section that soldier belongs to.
    identity_check = db.Column(db.Text)#USed to verify soldiers identity.
    vitals_history = db.relationship('Vitals', backref='soldier', lazy='dynamic')#Link  to table that  lists soldiers heart rate over time.
    location_history = db.relationship('Location', backref='soldier', lazy='dynamic')#Link to table that lists soldiers location over times.
    current_location = db.Column(db.Text)#Stores current location of soldier.
    last_heart_rate = db.Column(db.Integer)#Stores most recent record of soldiers location.
    last_update_time = db.Column(db.Text)#Stores time of last update.
    ammunition_expended = db.Column(db.Integer)#Stores number of rounds fired by soldier.
    rifle_sensor_battery_level = db.Column(db.Text)#Stores battery level of Ammunition tracker.
    status = db.Column(db.Text)#Stores Status of soldier.
    armour_sensor_battery_level = db.Column(db.Text)#Stores battery level of body armour sensor.
    hub_sensor_battery_level = db.Column(db.Text)#Battery level of sensor hub.
    distance_traveled = db.Column(db.Text)#Stores distance traveled by soldier.


    def __init__(self,id,name,role,section_id):
        """
        Initializes a new section member.

        To add a soldier, it requires an entry of an army number, a name,
        the role in the section, and the section they belong to.

        Args:
            id (int): Army number, must be unique.
            name (str): Soldier's name.
            role (str): Soldier's role in the section.
            section_id (int): Section the soldier belongs to.
        """
        self.id = id#Army number.
        self.name=name#Soldiers name.
        self.role=role#Soldiers role in the section.
        self.section_id = section_id#Section soldier belongs to.


class Vitals(db.Model):
    """
    Represents a table for recording a soldier's vital signs, particularly heart rate.

    This class corresponds to the 'vitals' table in the database.

    Attributes:
        id (int): Automatically generated unique primary key for the database entry.
        heart_rate (int): Heart rate of the soldier.
        update_time (str): Time when the heart rate entry was made.
        soldier_id (int): ID number of the soldier to whom the entry belongs.

    Methods:
        __init__(self, heart_rate, update_time, soldier_id):
            Initializes a new entry for heart rate for a soldier.

    """

    __tablename__='vitals'#Name of table.

    id = db.Column(db.Integer, primary_key=True)#ID number of entry in database. automatically generated unique primary key.
    heart_rate = db.Column(db.Integer)#Heart rate of soldier.
    update_time = db.Column(db.Text)#Time that heart rate entry was made.
    soldier_id = db.Column(db.Integer,db.ForeignKey('soldiers.id'))#ID number of Soldier.
    #soldier = db.relationship('Soldier', backref='vitals_history', lazy='dynamic')

    #function used to create a new entry for heart rate for soldier.Automatically created from data sent from sensors.
    def __init__(self, heart_rate, time, soldier_id):
        """
        Initializes a new entry for heart rate for a soldier.

        Parameters:
            heart_rate (int): Heart rate.
            update_time (str): Time of the entry.
            soldier_id (int): ID number of the soldier that the entry belongs to.
        """

        self.heart_rate = heart_rate#Heart rate.
        self.update_time = time#Time of entry.
        self.soldier_id = soldier_id#ID number of soldier that the entry belongs to.



class Location(db.Model):
    """
    Represents a table for recording the locations a soldier has been.

    This class corresponds to the 'locations' table in the database.

    Attributes:
        id (int): Automatically generated unique primary key for the database entry.
        long (str): Longitude of the soldier's location.
        lat (str): Latitude of the soldier's location.
        grid_reference (str): Grid reference of the soldier's location.
        update_time (str): Time when the location entry was made.
        soldier_id (int): ID number of the soldier to whom the entry belongs.

    Methods:
        __init__(self, long, lat, grid_reference, update_time, soldier_id):
            Initializes a new entry for the location of a soldier.

    """

    __tablename__ = 'locations'#Table name.

    id = db.Column(db.Integer, primary_key=True)#ID number of entry in database. automatically generated unique primary key.
    long = db.Column(db.Text)#longitude.
    lat = db.Column(db.Text)#latitude.
    grid_reference = db.Column(db.Text)#Grid reference
    update_time = db.Column(db.Text)#Time that location entry was made.
    soldier_id = db.Column(db.Integer,db.ForeignKey('soldiers.id'))#ID number of soldier that the entry belongs to.
    #soldier = db.relationship('Soldier', backref='location_history', lazy='dynamic')

    #function used to create a new entry for location of soldier.Automatically created from data sent from sensors.
    def __init__(self,long,lat,grid,time,soldier_id):
         """
        Initializes a new entry for the location of a soldier.

        Parameters:
            long (str): Longitude of the soldier's location.
            lat (str): Latitude of the soldier's location.
            grid_reference (str): Grid reference of the soldier's location.
            update_time (str): Time when the location entry was made.
            soldier_id (int): ID number of the soldier to whom the entry belongs.
        """
         self.long = long#Longitude.
         self.lat =lat#Latitude.
         self.grid_reference = grid#Grid reference.
         self.update_time = time#Time location entry was made.
         self.soldier_id = soldier_id#ID number of soldier that the entry belongs to.



################################################
############View Functions#####################

@app.route('/')#flask app displays home page
def index():
    """
    Flask Route: '/'

    Function to handle requests to the home page ('/'). This function is called when the root URL is accessed
    by the Flask app. It renders the 'home.html' template and returns the HTML page to be displayed to the user.

    Returns:
    - str: Rendered HTML page ('index.html').
    """
    return render_template('index.html')#Returns 'home.html' to be displayed to user.

@app.route('/add-section', methods=['GET','POST'])#function to add a section
def add_section():
    """
    Flask Route: '/add-section' (GET and POST)

    Function to handle requests for adding a new section. This function is called when the '/add-section' URL is
    accessed by the Flask app, and it supports both GET and POST methods. It uses the 'CreateSection' form to gather
    user input.

    If the form is validated on submission, it extracts the section's ID and ammunition from the form, creates a new
    section with default values, and adds it to the database. Then, it redirects to the 'SectionOverview' page.

    Returns:
    - str: Rendered HTML page ('add-section.html') with the 'CreateSection' form for creating a new section.
            Or, redirects to the 'SectionOverview' page if a new section is successfully added.
    """
    form = CreateSection()#adds CreateSection form to be used in function.

    if form.validate_on_submit():#if the form is validated when the submit button is pressed.

        id  = form.id.data#Extracts id number from data entered in form.
        SectionAmmo = form.SectionAmmo.data#Extracts Ammunition from data entered in form.

        new_sec=Section(id,SectionAmmo)#Creates new section member form data entered in form.
        new_sec.section_strength = 0#Sets initial value of section strength to 0.
        new_sec.section_ok = 0#Sets initial value of SectionOK to 0.
        new_sec.section_casualty = 0#Sets initial value of Casualties in section to 0.
        new_sec.section_location = "0"#Sets initial value of location to 0.
        new_sec.section_battery = "100"#Sets initial value of Battery to to 100.
        db.session.add(new_sec)#Takes object created from data taken from form and adds it to database.
        db.session.commit()#Saves change made to database.



        return redirect(url_for('SectionOverview'))#Redirects to page that displays Section information.


    return render_template('add-section.html',form=form)#Returns Html page for form to create a new section.

@app.route('/Addamunition', methods=['GET','POST'])#function to add a section
def add_ammo():
    """
    Flask Route: '/Addamunition' (GET and POST)

    Function to handle requests for adding ammunition to a section. This function is called when the '/Addamunition'
    URL is accessed by the Flask app, and it supports both GET and POST methods. It uses the 'Addammo' form to gather
    user input.

    If the form is validated on submission, it extracts the section's ID and ammunition from the form, queries the
    database to get the corresponding section, adds the ammunition to the section, and updates the database. Then, it
    redirects to the 'SectionOverview' page.

    Returns:
    - str: Rendered HTML page ('Addamunition.html') with the 'Addammo' form for adding ammunition to a section.
            Or, redirects to the 'SectionOverview' page if ammunition is successfully added to the section.
    """
    form = Addammo()#adds form to be used in function.

    if form.validate_on_submit():#if the form is validated when the submit button is pressed.

        id  = form.id.data#Extracts id number from data entered in form
        amuntion_added = form.SectionAmmo.data#Extracts ammunition from data enter in form.

        resupply=Section.query.get_or_404(id) #Queries database using entered id number returns 404 message if number entered is not in database.
        resupply.section_amunition = resupply.section_amunition + amuntion_added #Takes ammunition added in form and adds it to section ammunition.
        db.session.add(resupply) #Adds new entry to database.
        db.session.commit() #Saves change to database.


        return redirect(url_for('SectionOverview'))#redirects to page that displays section information.


    return render_template('Addamunition.html',form=form) #returns html page that displays page to add ammunition to section.

@app.route('/SectionOverview') #Displays section overview to user
def SectionOverview():
    """
    Flask Route: '/SectionOverview'

    Function to handle requests for displaying the section overview to the user. This function is called when the
    '/SectionOverview' URL is accessed by the Flask app.

    Returns:
    - str: Rendered HTML page ('SectionOverview.html') containing the overview of the section.
    """

    return render_template('SectionOverview.html')#Returns html page for overview of section.


@app.route('/deleteSection',methods = ['POST','GET'])#Remove section
def deleteSection():
    """
    Route handler to remove a section along with its associated soldiers.

    This function handles HTTP GET and POST requests for deleting a section. If the provided form is validated,
    it extracts the section ID and deletes all soldiers associated with that section. Finally, it deletes the
    specified section from the database.

    Parameters:
    - None

    Returns:
    - GET Request: Renders the 'deleteSection.html' template with the deletion form.
    - POST Request: Redirects to the 'SectionOverview' route after successfully deleting the section and associated soldiers.
    """
    
    form =DelSection()#adds form to be used in function.

    if form.validate_on_submit():#if the form is validated when the submit button is pressed.
        id = form.id.data#Extracts id number from data entered in form

        soldiers = Soldier.query.filter_by(section_id = id).all()#When section is deleted. Queries all soldiers with same section id and deletes them.
        for i in soldiers:#for loop to iterate through soldiers returned by query.
            db.session.delete(i)#deletes soldier.
            db.session.commit()#saves change to database.


        section = Section.query.get_or_404(id)#Queries section using entered id data taken from form. Returns 404 message if no entry exists.
        db.session.delete(section)#Deletes section.
        db.session.commit()#Saves change to database.



        return redirect(url_for('SectionOverview'))#redirects to page that displays section information.
    return render_template('deleteSection.html',form=form)#Returns html page of form to delete section.


@app.route('/add', methods=['GET','POST'])#add person to section,uses army number as primary key to add member to section. initial values automatically given.
def add_soldier():
    """
    Flask Route: '/add'

    Function to handle requests for adding a new soldier to a section. This function is called when the '/add' URL is accessed
    by the Flask app. The function processes the form data submitted, creates a new soldier entry, and updates the section
    information accordingly.

    Returns:
    - str or redirect: If the form is successfully validated and the soldier is added, it redirects to the 'list' page. If not,
      it returns the HTML page ('add.html') for adding a new member to the section.
    """
    form = AddForm()#adds form to be used in function.

    if form.validate_on_submit():#if the form is validated when the submit button is pressed.

        id = form.id.data#Extracts id number from data entered in form
        name = form.name.data#Extracts Soldiers name from data entered in form.
        role = form.role.data#Extracts Soldiers role from data entered in form.
        section_id = form.section_id.data#Extracts Soldiers Section id from data entered in form.

        new_sol=Soldier(id,name,role,section_id)#Creates new soldier using data entered in form.
        new_sol.identity_check = "Unverified"#Sets initial for Identity verification.
        new_sol.last_update_time = datetime.datetime.now().strftime("%X")#Sets initial for time using time extracted from computer clock.
        new_sol.ammunition_expended = 0#Sets initial value for ammunition fired by soldier to 0.
        new_sol.last_heart_rate = 0#Sets initial value for heart rate to 0.
        new_sol.current_location = "0"#Sets initial value for location TO 0.
        new_sol.rifle_sensor_battery_level = "100"#Sets initial value for rifle battery to 100.
        new_sol.status = "OK"#Sets initial value for State to "OK".
        new_sol.armour_sensor_battery_level = "100"#Sets initial value for Armour battery to 100.
        new_sol.distance_traveled ="0"#Sets initial values for Distance traveled to 0.
        new_sol.hub_sensor_battery_level="100"#Sets initial value for HubBattery to 100.
        db.session.add(new_sol)#adds soldier to database.
        db.session.commit()#Saves change to database.

        update_section = Section.query.get(section_id)#Queries Section table using section id of soldier.
        update_section.section_strength = update_section.section_strength + 1#Adds one to section Strength for new person added to section.
        update_section.section_ok = update_section.section_ok + 1#Adds one person to SectionOK for new person added to section.
        db.session.add(update_section)#Adds updated information to database.
        db.session.commit()#Saves change to database.


        return redirect(url_for('list'))#Redirects to html page that displays List of section members.


    return render_template('add.html',form=form)#returns html page for form to add member to section.

@app.route('/listHeartRate/<id>')#display  list of soldiers heart rate to user
def listHeartRate(id):
    """
    Flask Route: '/listHeartRate/<id>'

    Function to handle requests for displaying a list of a soldier's heart rates. This function is called when the '/listHeartRate'
    URL is accessed by the Flask app. It queries the database for all heart rate entries associated with the given soldier ID and also
    retrieves the soldier's information. The data is then passed to the 'listHeartRate.html' template for rendering.

    Args:
    - id (str): Soldier ID for whom the heart rates are to be listed.

    Returns:
    - render_template: HTML page ('listHeartRate.html') that displays the list of heart rate entries for the selected soldier.
    """

    Heart = Vitals.query.filter_by(soldier_id = id ).all()#Queries all Entries in vitals table with soldier_id entered by user.
    person = Soldier.query.get_or_404(id)#Queries soldier using id number entered by user. Returns 404 message is entered id number does not exist in database.


    return render_template('listHeartRate.html', Heart = Heart, person = person)#Returns html page that lists vitals entries of selected soldier.

@app.route('/ViewHeart',methods = ['POST','GET'])#select which section members heart rate to view
def ViewHeart():
    """
    Flask Route: '/ViewHeart'

    Function to handle requests for selecting which section member's heart rate to view. This function is called when the '/ViewHeart'
    URL is accessed by the Flask app. It uses a form ('HeartForm') to get the ID number of the soldier for whom the heart rate entries
    need to be viewed. If the form is validated, the function redirects to the 'listHeartRate' page for the selected soldier. Otherwise,
    it renders the 'ViewHeart.html' template, which includes the form for soldier selection.

    Returns:
    - redirect or render_template: If the form is validated, redirects to the 'listHeartRate' page. Otherwise, renders 'ViewHeart.html'
      with the soldier selection form.
    """
    form =HeartForm()#adds form to be used in function.

    if form.validate_on_submit():#if the form is validated when the submit button is pressed.
        id = form.id.data#Extracts id number from data entered in form

        return redirect(url_for('listHeartRate', id = id))#Redirects to html page to display vitals table entries for entered id number.
    return render_template('ViewHeart.html',form=form)#Displays html page that for form to select soldier to view their vitals table entries.

@app.route('/listLocation/<id>')#Select soldier to view  locations soldier has been
def listLocation(id):
    """
    Flask Route: '/listLocation/<id>'

    Function to handle requests for selecting a soldier to view the locations they have been. This function is called when the '/listLocation'
    URL is accessed by the Flask app. It queries the 'location' table to retrieve all entries with the soldier_id entered by the user. It also
    queries the 'Soldier' table to get information about the soldier with the entered id. If the soldier does not exist, a 404 message is
    returned. The function then renders the 'listLocation.html' template, which displays a list of all locations the soldier has been.

    Args:
    - id (int): The ID number of the soldier for whom the locations are to be viewed.

    Returns:
    - render_template: HTML page to display a list of all locations the soldier has been, along with relevant information about the soldier.
    """

    Location = Location.query.filter_by(soldier_id = id ).all()#Queries all Entries in location table with soldier_id entered by user.
    person = Soldier.query.get_or_404(id)#Queries soldier using id number entered by user. Returns 404 message is entered id number does not exist in database.
    return render_template('listLocation.html', Location = Location, person = person)#returns html page to display list of all locations soldier has been.

@app.route('/ViewLocation',methods = ['POST','GET'])#displays locations soldier has been
def ViewLocation():
    """
    Flask Route: '/ViewLocation'

    Function to handle requests for displaying the locations a soldier has been. This function is called when the '/ViewLocation'
    URL is accessed by the Flask app. It uses the 'LocationForm' to get the soldier's ID from the user. If the form is validated upon
    submission, the function redirects to the 'listLocation' route, passing the soldier's ID. This route displays a list of all
    locations the soldier has been.

    Returns:
    - render_template: HTML page containing the form to select a soldier to view their locations.
    - redirect: If the form is validated, redirects to the 'listLocation' route to display the locations of the selected soldier.
    """
    form =LocationForm()#adds form to be used in function.

    if form.validate_on_submit():#if the form is validated when the submit button is pressed.
        id = form.id.data#Extracts id number from data entered in form

        return redirect(url_for('listLocation', id = id))#Redirects to webpage to display list of soldiers locations.
    return render_template('ViewLocation.html',form=form)#Returns html for form to select soldier.



@app.route('/list')#list all members in section
def list():
    """
    Flask Route: '/list'

    Function to handle requests for listing all members in a section. This function is called when the '/list' URL is accessed
    by the Flask app. It returns an HTML page ('list.html') that displays a list of soldiers in the section.

    Returns:
    - render_template: HTML page for displaying the list of soldiers in the section.
    """

    return render_template('list.html')#Returns html page that that displays soldiers in section.


@app.route('/section', methods = ['GET'])#sends section information to a page in json script format.
def Sectionj_stuff():
    """
    Flask Route: '/section'

    Function to handle requests for section information in JSON script format. This function is called when the '/section'
    URL is accessed by the Flask app using the GET method. It queries all section information from the database, formats it
    into a list of dictionaries, each representing a section, and returns the result as a JSON script.

    Returns:
    - str: JSON script containing section information, formatted as a list of dictionaries.
    """

    section = Section.query.all()#Queries all section information.

    sections = []#blank list to store json information.
    for i in section:#For loop to iterate through Queried data and store it in a list printed in json format.
            soldier = {"id": i.id,"SectionAmmo":i.section_amunition,"SectionStrength":i.section_strength,"SectionLocation":i.section_location,
                        "SectionOK":i.section_ok,"SectionCasualty":i.section_casualty,"SectionBattery":i.section_battery}#Queried information printed as json.
            sections.append(soldier)#information appended to list.

    #print(json.dumps(sections))
    return json.dumps(sections)#list converted to json and printed to page'/section'


@app.route('/soldiers', methods = ['GET'])#sends section information to a page in json script format.
def Soldierj_stuff():
    """
    Flask Route: '/soldiers'

    Function to handle requests for soldier information in JSON script format. This function is called when the '/soldiers'
    URL is accessed by the Flask app using the GET method. It queries all soldier information from the database, formats it
    into a list of dictionaries, each representing a soldier, and returns the result as a JSON script.

    Returns:
    - str: JSON script containing soldier information, formatted as a list of dictionaries.
    """

    section = Soldier.query.all()#Queries all Soldier information.

    sections = []#blank list to store json information.
    for i in section:#For loop to iterate through Queried data and store it in a list printed in json format.
            soldier = {"id": i.id,"name":i.name,"role": i.role,"Ident":i.identity_check,"LastHR":i.last_heart_rate,"currentLocation":i.current_location,
                        "Distance":i.distance_traveled,"TIME":i.last_update_time,"Rndsfired":i.ammunition_expended,"RifleBat":i.rifle_sensor_battery_level,"State":i.status,
                        "ArmourBat":i.armour_sensor_battery_level, "HubBattery":i.hub_sensor_battery_level}#Queried information printed as json.
            sections.append(soldier)#information appended to list.

    #print(json.dumps(sections))
    return json.dumps(sections)#list converted to json and printed to page'/section'



@app.route('/delete',methods = ['POST','GET'])#remove soldier from section
def del_soldier():
    """
    Flask Route: '/delete'

    Function to handle requests for removing a soldier from a section. This function is called when the '/delete' URL
    is accessed by the Flask app using the POST or GET method. It uses a form to get the soldier's ID, queries the
    Soldier table using the ID, deletes the soldier's entry from the database, and updates the section information
    accordingly.

    Returns:
    - redirect: Redirects to the '/list' URL to display the updated section information.

    HTML Template:
    - 'delete.html': Returns HTML page for the form to delete a section member if the form is not validated.
    """
    form =DelForm()#adds form to be used in function.

    if form.validate_on_submit():#if the form is validated when the submit button is pressed.
        id = form.id.data#Extracts id number from data entered in form
        soldier = Soldier.query.get_or_404(id)#Queries Soldiers table using entered id returns 404 message id query does not exist.
        db.session.delete(soldier)#Deletes entry from database.
        db.session.commit()#Saves change to database.

        update_section = Section.query.get(soldier.section_id)#Queries Section table using section id of soldier.
        update_section.section_strength -= 1#Takes one from section Strength for person removed from section.
        update_section.section_ok -= 1#Takes one from section Ok for person removed from section..
        db.session.add(update_section)#Adds updated information to database.
        db.session.commit()#Saves change to database.

        return redirect(url_for('list'))#Redirects to page to display section information.
    return render_template('delete.html',form=form)#Returns html page for form to delete section member.


@app.route('/input/<message>')#takes information sent by arduino and updated  database
def input(message):
    """
    Flask Route: '/input/<message>'

    Function to handle requests for updating the database with information sent by Arduino. This function is called when
    the '/input/<message>' URL is accessed by the Flask app. The Arduino sends data, which is converted into a dictionary
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
    - Accessing '/input/123456?HR=80&Ident=1&long=40.7128&lat=-74.0060&TIME=12:00&Rndsfired=5&RifleBat=80&State=1&ArmourBat=90'
      would update the database for the soldier with ID 123456 based on the provided data.
    """

    message_dict = Convert(message)#calls function to convert data sent from arduino to dictionary.

    Update = Soldier.query.get(message_dict['id'])#Queries database for using id number stored in dictionary.

    Update.TIME = datetime.datetime.now().strftime("%X")#Updates time of last entry using computer clock.
    db.session.add(Update)#Stores update to database.
    db.session.commit()#Saves change to database.

    if 'Ident'in message_dict:#Checks dict for Identity check.
        if message_dict['Ident'] == "1":#if arduino sends 1 identity is verified.
            Update.Ident = "Verified"#Updates identity as verified.
            db.session.add(Update)#Stores update to database.
            db.session.commit()#Saves change to database.
        else:
            Update.Ident = "Unverified"#Updates identity as unverified.
            db.session.add(Update)#Stores update to database.
            db.session.commit()#Saves change to database.

    if 'HR'in message_dict:#Checks dict for heart rate
        Update.LastHR = message_dict['HR']#Updates database using information in dictionary
        db.session.add(Update)#Stores update to database.
        db.session.commit()#Saves change to database.

        #Creates new entry in vitals table using data received from arduino and time from computer clock.
        newVital = Vitals(message_dict['HR'],datetime.datetime.now().strftime("%X"),message_dict['id'])
        db.session.add(newVital)#Stores update to database.
        db.session.commit()#Saves change to database.

    if 'long' and 'lat' in message_dict:#Checks dict for latitude and longitude.
        Update.currentLocation = OS_GRID(float(message_dict['lat']),float(message_dict['long']))#converts lat and long to grid reference.
        db.session.add(Update)#Stores update to database.
        db.session.commit()#Saves change to database.

        #Creates new entry in location table using data received from arduino and time from computer clock.
        new_location = Location(message_dict['long'],message_dict['lat'],OS_GRID(float(message_dict['lat']),float(message_dict['long'])),datetime.datetime.now().strftime("%X"),message_dict['id'])
        db.session.add(new_location)#Stores update to database.
        db.session.commit()#Saves change to database.

        if Update.role == "I/C":#If the role of the soldier is the section I/C then their location is used for section location.
            updateSection = Section.query.get(Update.section_id)#queries Section table using Section ID of soldier.
            updateSection.SectionLocation = Update.currentLocation#Sets section location to Section commanders current location.
            db.session.add(updateSection)#Stores update to database.
            db.session.commit()#Saves change to database.

        Traveled = Location.query.filter_by(soldier_id =message_dict['id']).all()#Queries table of locations using Id number of soldier and returns all entries.
        if len(Traveled)>1:#If there is more that one entry for location gets the distance between those locations.
            dist = 0#Stores distance traveled.
            i = 0#used to increment through array in while loop.
            while i < len(Traveled):#increments through list of locations getting the distance between two points at each increment.
                if i == (len(Traveled)-1):#breaks from loop on second last entry otherwise an error is caused.
                    break
                else:#adds distance between the two points currently being calculated and adds them to total distance.
                    #Function distance.distance() taken from package geopy. Takes two latitude longitude points as an argument,
                    #returns the distance between those two points, the .m at the end of the function has selected the returned value to be in meters.
                    dist = dist + distance.distance([float(Traveled[i].lat),float(Traveled[i].long)],[float(Traveled[i+1].lat),float(Traveled[i+1].long)]).m
                i = i + 1#used to increment through list.
            if dist > 1000:#if the distance in meters is greater than 1000 converts to Km
                            #round() function used to keep answer to 3 decimal places.
                dist = str(round(dist/1000.0,3)) + "Km"
            else:
                dist = str(round(dist,3)) + "m"

            updateDistance = Soldier.query.get(message_dict['id'])#Queries database using soldiers Id
            updateDistance.Distance = dist #updates distance traveled.
            db.session.add(updateDistance)#Stors update to database.
            db.session.commit()#Saves change to database.

        #This was used when I would get the time of an update from the GPS RTC.
    if 'TIME'in message_dict:#Checks dict for TIME
        Update.TIME = message_dict['TIME']#Updates database using information in dictionary
        db.session.add(Update)#Stores update to database.
        db.session.commit()#Saves change to database.

    if 'Rndsfired'in message_dict:#Checks dict for ammunition fired
        Update.Rndsfired = Update.Rndsfired + message_dict['Rndsfired']#Updates database using information in dictionary
        db.session.add(Update)#Stores update to database.
        db.session.commit()#Saves change to database.

        update_section_ammo = Section.query.get(Update.section_id)#Queries Section table using section id of soldier.
        #updates total of ammunition left in the section base on rounds fired by th soldier.
        update_section_ammo.SectionAmmo = update_section_ammo.SectionAmmo - message_dict['Rndsfired']
        db.session.add(update_section_ammo)#Stores update to database.
        db.session.commit()#Saves change to database.

    if 'RifleBat'in message_dict:#Checks dict for Rifle battery information.
        Update.RifleBat = message_dict['RifleBat']#Updates database using information in dictionary
        db.session.add(Update)#Stores update to database.
        db.session.commit()#Saves change to database.

    if 'State'in message_dict:#Checks dict for if body armour sensor was triggered.
        if message_dict['State'] == "1":#If 'State' is set to '1' sensor has been triggered.
            Update.State = "Casualty"#changes value in 'State' to 'Casualty'.
            db.session.add(Update)#Stores update to database.
            db.session.commit()#Saves change to database.

            SectionCas = Section.query.get(Update.section_id)#Queries Section table using section id of soldier.
            SectionCas.SectionCasualty = SectionCas.SectionCasualty + 1#Adds 1 to Casualty in section table.
            SectionCas.SectionOK = SectionCas.SectionOK - 1#Removes 1 from section ok.
            db.session.add(SectionCas)#Stores update to database.
            db.session.commit()#Saves change to database.

        else:
            Update.State = "OK"#State is OK
            db.session.add(Update)#Stores update to database.
            db.session.commit()#Saves change to database.

    if 'ArmourBat'in message_dict:#Checks dict for Body armour battery level.
        Update.ArmourBat = message_dict['ArmourBat']#Updates database using information in dictionary
        db.session.add(Update)#Stores update to database.
        db.session.commit()#Saves change to database.

    return "ok" #message returned to arduino by server.




if __name__=='__main__':#if python is run as main file.
    app.run(debug=True)#turns on debugger used while testing code on laptop.
    #app.run(host = '0.0.0.0',port = '5000')#Allows access to server when set to'0.0.0.0' uncomment to when running on raspberry pi.
