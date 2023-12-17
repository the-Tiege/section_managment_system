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
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basdir,'SectionDB.sqlite')#creates sqlite database in same folder.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False#turn off modification tracking.

db = SQLAlchemy(app)#create Sqlalchemy app.
Migrate(app,db)#create migration object.

##########Tables#########################

class Section(db.Model):#Table for overview of section, tracks overall state of the section.

    __tablename__ = 'Section'#name of the table.

    id = db.Column(db.Integer,primary_key = True)#section number used as primary key.
    SectionAmmo = db.Column(db.Integer)#total ammunition in the section.
    SectionStrength = db.Column(db.Integer)#Number of people in the section.
    SectionOK = db.Column(db.Integer)#Soldiers in section who are uninjured.
    SectionCasualty = db.Column(db.Integer)#Soldiers in section who have become casualties.
    SectionLocation = db.Column(db.Text)#Location of section, Taken from section commanders location.
    SectionBattery = db.Column(db.Text)#battery level indication for Section database.
    Soldier = db.relationship('Soldier', backref = 'section', lazy='dynamic')#relationship to table soldiers.

    def __init__(self,id,SectionAmmo):#function used to create a new section. To create the section it requires an entry of an id number and ammunition.
        self.id = id#Identifying number of the section must be unique.
        self.SectionAmmo = SectionAmmo#Sections starting ammunition.


class Soldier(db.Model):#Table for soldiers in section, gives more detailed information on each soldier.

    __tablename__='soldiers'#Table name.

    id = db.Column(db.Integer,primary_key=True)#Army number  of soldier primary key. Must be unique.
    name = db.Column(db.Text)#Soldiers name.
    role = db.Column(db.Text)#Role of section member.
    section_id = db.Column(db.Integer,db.ForeignKey('Section.id'))#ID number of section that soldier belongs to.
    Ident = db.Column(db.Text)#USed to verify soldiers identity.
    vitals = db.relationship('vitals',backref = 'soldiers', lazy = 'dynamic')#Link  to table that  lists soldiers heart rate over time.
    location = db.relationship('location', backref = 'soldiers', lazy = 'dynamic')#Link to table that lists soldiers location over times.
    currentLocation = db.Column(db.Text)#Stores current location of soldier.
    LastHR = db.Column(db.Integer)#Stores most recent record of soldiers location.
    TIME = db.Column(db.Text)#Stores time of last update.
    Rndsfired = db.Column(db.Integer)#Stores number of rounds fired by soldier.
    RifleBat = db.Column(db.Text)#Stores battery level of Ammunition tracker.
    State = db.Column(db.Text)#Stores Status of soldier.
    ArmourBat = db.Column(db.Text)#Stores battery level of body armour sensor.
    HubBattery = db.Column(db.Text)#Battery level of sensor hub.
    Distance = db.Column(db.Text)#Stores distance traveled by soldier.

    #function used to create a new section Member. To add Soldier requires an entry of an id number, a name, Role in the section and the section they are in.
    def __init__(self,id,name,role,section_id):
        self.id = id#Army number.
        self.name=name#Soldiers name.
        self.role=role#Soldiers role in the section.
        self.section_id = section_id#Section soldier belongs to.


class vitals(db.Model):#table for record of soldiers vital signs

    __tablename__='vitals'#Name of table.

    id = db.Column(db.Integer, primary_key=True)#ID number of entry in database. automatically generated unique primary key.
    HR = db.Column(db.Integer)#Heart rate of soldier.
    TIME = db.Column(db.Text)#Time that heart rate entry was made.
    soldier_id = db.Column(db.Integer,db.ForeignKey('soldiers.id'))#ID number of Soldier.

    #function used to create a new entry for heart rate for soldier.Automatically created from data sent from sensors.
    def __init__(self,HR,TIME,soldier_id):
        self.HR = HR#Heart rate.
        self.TIME = TIME#Time of entry.
        self.soldier_id = soldier_id#ID number of soldier that the entry belongs to.



class location(db.Model):#table for record of all locations soldiers has been

    __tablename__ = 'locations'#Table name.

    id = db.Column(db.Integer, primary_key=True)#ID number of entry in database. automatically generated unique primary key.
    long = db.Column(db.Text)#longitude.
    lat = db.Column(db.Text)#latitude.
    GRID = db.Column(db.Text)#Grid reference
    TIME = db.Column(db.Text)#Time that heart rate entry was made.
    soldier_id = db.Column(db.Integer,db.ForeignKey('soldiers.id'))#ID number of soldier that the entry belongs to.

    #function used to create a new entry for location of soldier.Automatically created from data sent from sensors.
    def __init__(self,long,lat,GRID,TIME,soldier_id):
         self.long = long#Longitude.
         self.lat =lat#Latitude.
         self.GRID = GRID#Grid reference.
         self.TIME = TIME#Time location entry was made.
         self.soldier_id = soldier_id#ID number of soldier that the entry belongs to.



################################################
############View Functions#####################

@app.route('/')#flask app displays home page
def index():#function called when '/' called by flask app.
    return render_template('home.html')#Returns 'home.html' to be displayed to user.

@app.route('/newSection', methods=['GET','POST'])#function to add a section
def add_section():#function called when '/newSection' called by flask app.
    form = CreateSection()#adds CreateSection form to be used in function.

    if form.validate_on_submit():#if the form is validated when the submit button is pressed.

        id  = form.id.data#Extracts id number from data entered in form.
        SectionAmmo = form.SectionAmmo.data#Extracts Ammunition from data entered in form.

        new_sec=Section(id,SectionAmmo)#Creates new section member form data entered in form.
        new_sec.SectionStrength = 0#Sets initial value of section strength to 0.
        new_sec.SectionOK = 0#Sets initial value of SectionOK to 0.
        new_sec.SectionCasualty = 0#Sets initial value of Casualties in section to 0.
        new_sec.SectionLocation = "0"#Sets initial value of location to 0.
        new_sec.SectionBattery = "100"#Sets initial value of Battery to to 100.
        db.session.add(new_sec)#Takes object created from data taken from form and adds it to database.
        db.session.commit()#Saves change made to database.



        return redirect(url_for('SectionOverview'))#Redirects to page that displays Section information.


    return render_template('newSection.html',form=form)#Returns Html page for form to create a new section.

@app.route('/Addamunition', methods=['GET','POST'])#function to add a section
def add_ammo():#function called when '/Addamunition' called by flask app.
    form = Addammo()#adds form to be used in function.

    if form.validate_on_submit():#if the form is validated when the submit button is pressed.

        id  = form.id.data#Extracts id number from data entered in form
        SectionAmmo = form.SectionAmmo.data#Extracts ammunition from data enter in form.

        resupply=Section.query.get_or_404(id)#Queries database using entered id number returns 404 message if number entered is not in database.
        resupply.SectionAmmo = resupply.SectionAmmo + SectionAmmo#Takes ammunition added in form and adds it to section ammunition.
        db.session.add(resupply)#Adds new entry to database.
        db.session.commit()#Saves change to database.


        return redirect(url_for('SectionOverview'))#redirects to page that displays section information.


    return render_template('Addamunition.html',form=form)#returns html page that displays page to add ammunition to section.

@app.route('/SectionOverview')#Displays section overview to user
def SectionOverview():#function called when '/' called by flask app.

    return render_template('SectionOverview.html')#Returns html page for overview of section.


@app.route('/deleteSection',methods = ['POST','GET'])#Remove section
def deleteSection():#function called when '/deleteSection' called by flask app.
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
def add_soldier():#function called when '/add' called by flask app.
    form = AddForm()#adds form to be used in function.

    if form.validate_on_submit():#if the form is validated when the submit button is pressed.

        id = form.id.data#Extracts id number from data entered in form
        name = form.name.data#Extracts Soldiers name from data entered in form.
        role = form.role.data#Extracts Soldiers role from data entered in form.
        section_id = form.section_id.data#Extracts Soldiers Section id from data entered in form.

        new_sol=Soldier(id,name,role,section_id)#Creates new soldier using data entered in form.
        new_sol.Ident = "Unverified"#Sets initial for Identity verification.
        new_sol.TIME = datetime.datetime.now().strftime("%X")#Sets initial for time using time extracted from computer clock.
        new_sol.Rndsfired = 0#Sets initial value for ammunition fired by soldier to 0.
        new_sol.LastHR = 0#Sets initial value for heart rate to 0.
        new_sol.currentLocation = "0"#Sets initial value for location TO 0.
        new_sol.RifleBat = "100"#Sets initial value for rifle battery to 100.
        new_sol.State = "OK"#Sets initial value for State to "OK".
        new_sol.ArmourBat = "100"#Sets initial value for Armour battery to 100.
        new_sol.Distance ="0"#Sets initial values for Distance traveled to 0.
        new_sol.HubBattery="100"#Sets initial value for HubBattery to 100.
        db.session.add(new_sol)#adds soldier to database.
        db.session.commit()#Saves change to database.

        update_section = Section.query.get(section_id)#Queries Section table using section id of soldier.
        update_section.SectionStrength = update_section.SectionStrength + 1#Adds one to section Strength for new person added to section.
        update_section.SectionOK = update_section.SectionOK + 1#Adds one person to SectionOK for new person added to section.
        db.session.add(update_section)#Adds updated information to database.
        db.session.commit()#Saves change to database.


        return redirect(url_for('list'))#Redirects to html page that displays List of section members.


    return render_template('add.html',form=form)#returns html page for form to add member to section.

@app.route('/listHeartRate/<id>')#display  list of soldiers heart rate to user
def listHeartRate(id):#function called when '/listHeartRate' called by flask app.

    Heart = vitals.query.filter_by(soldier_id = id ).all()#Queries all Entries in vitals table with soldier_id entered by user.
    person = Soldier.query.get_or_404(id)#Queries soldier using id number entered by user. Returns 404 message is entered id number does not exist in database.


    return render_template('listHeartRate.html', Heart = Heart, person = person)#Returns html page that lists vitals entries of selected soldier.

@app.route('/ViewHeart',methods = ['POST','GET'])#select which section members heart rate to view
def ViewHeart():#function called when '/ViewHeart' called by flask app.
    form =HeartForm()#adds form to be used in function.

    if form.validate_on_submit():#if the form is validated when the submit button is pressed.
        id = form.id.data#Extracts id number from data entered in form

        return redirect(url_for('listHeartRate', id = id))#Redirects to html page to display vitals table entries for entered id number.
    return render_template('ViewHeart.html',form=form)#Displays html page that for form to select soldier to view their vitals table entries.

@app.route('/listLocation/<id>')#Select soldier to view  locations soldier has been
def listLocation(id):#function called when '/listLocation' called by flask app.

    Location = location.query.filter_by(soldier_id = id ).all()#Queries all Entries in location table with soldier_id entered by user.
    person = Soldier.query.get_or_404(id)#Queries soldier using id number entered by user. Returns 404 message is entered id number does not exist in database.
    return render_template('listLocation.html', Location = Location, person = person)#returns html page to display list of all locations soldier has been.

@app.route('/ViewLocation',methods = ['POST','GET'])#displays locations soldier has been
def ViewLocation():#function called when '/ViewLocation' called by flask app.
    form =LocationForm()#adds form to be used in function.

    if form.validate_on_submit():#if the form is validated when the submit button is pressed.
        id = form.id.data#Extracts id number from data entered in form

        return redirect(url_for('listLocation', id = id))#Redirects to webpage to display list of soldiers locations.
    return render_template('ViewLocation.html',form=form)#Returns html for form to select soldier.



@app.route('/list')#list all members in section
def list():#function called when '/list' called by flask app.

    return render_template('list.html')#Returns html page that that displays soldiers in section.


@app.route('/section', methods = ['GET'])#sends section information to a page in json script format.
def Sectionj_stuff():#function called when '/section' called by flask app.

    section = Section.query.all()#Queries all section information.

    sections = []#blank list to store json information.
    for i in section:#For loop to iterate through Queried data and store it in a list printed in json format.
            soldier = {"id": i.id,"SectionAmmo":i.SectionAmmo,"SectionStrength":i.SectionStrength,"SectionLocation":i.SectionLocation,
                        "SectionOK":i.SectionOK,"SectionCasualty":i.SectionCasualty,"SectionBattery":i.SectionBattery}#Queried information printed as json.
            sections.append(soldier)#information appended to list.

    #print(json.dumps(sections))
    return json.dumps(sections)#list converted to json and printed to page'/section'


@app.route('/soldiers', methods = ['GET'])#sends section information to a page in json script format.
def Soldierj_stuff():#function called when '/soldiers' called by flask app.

    section = Soldier.query.all()#Queries all Soldier information.

    sections = []#blank list to store json information.
    for i in section:#For loop to iterate through Queried data and store it in a list printed in json format.
            soldier = {"id": i.id,"name":i.name,"role": i.role,"Ident":i.Ident,"LastHR":i.LastHR,"currentLocation":i.currentLocation,
                        "Distance":i.Distance,"TIME":i.TIME,"Rndsfired":i.Rndsfired,"RifleBat":i.RifleBat,"State":i.State,
                        "ArmourBat":i.ArmourBat, "HubBattery":i.HubBattery}#Queried information printed as json.
            sections.append(soldier)#information appended to list.

    #print(json.dumps(sections))
    return json.dumps(sections)#list converted to json and printed to page'/section'



@app.route('/delete',methods = ['POST','GET'])#remove soldier from section
def del_soldier():#function called when '/delete' called by flask app.
    form =DelForm()#adds form to be used in function.

    if form.validate_on_submit():#if the form is validated when the submit button is pressed.
        id = form.id.data#Extracts id number from data entered in form
        soldier = Soldier.query.get_or_404(id)#Queries Soldiers table using entered id returns 404 message id query does not exist.
        db.session.delete(soldier)#Deletes entry from database.
        db.session.commit()#Saves change to database.

        update_section = Section.query.get(soldier.section_id)#Queries Section table using section id of soldier.
        update_section.SectionStrength = update_section.SectionStrength - 1#Takes one from section Strength for person removed from section.
        update_section.SectionOK = update_section.SectionOK - 1#Takes one from section Ok for person removed from section..
        db.session.add(update_section)#Adds updated information to database.
        db.session.commit()#Saves change to database.

        return redirect(url_for('list'))#Redirects to page to display section information.
    return render_template('delete.html',form=form)#Returns html page for form to delete section member.


@app.route('/input/<message>')#takes information sent by arduino and updated  database
def input(message):#function called when '/' called by flask app.

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
        newVital = vitals(message_dict['HR'],datetime.datetime.now().strftime("%X"),message_dict['id'])
        db.session.add(newVital)#Stores update to database.
        db.session.commit()#Saves change to database.

    if 'long' and 'lat' in message_dict:#Checks dict for latitude and longitude.
        Update.currentLocation = OS_GRID(float(message_dict['lat']),float(message_dict['long']))#converts lat and long to grid reference.
        db.session.add(Update)#Stores update to database.
        db.session.commit()#Saves change to database.

        #Creates new entry in location table using data received from arduino and time from computer clock.
        new_location = location(message_dict['long'],message_dict['lat'],OS_GRID(float(message_dict['lat']),float(message_dict['long'])),datetime.datetime.now().strftime("%X"),message_dict['id'])
        db.session.add(new_location)#Stores update to database.
        db.session.commit()#Saves change to database.

        if Update.role == "I/C":#If the role of the soldier is the section I/C then their location is used for section location.
            updateSection = Section.query.get(Update.section_id)#queries Section table using Section ID of soldier.
            updateSection.SectionLocation = Update.currentLocation#Sets section location to Section commanders current location.
            db.session.add(updateSection)#Stores update to database.
            db.session.commit()#Saves change to database.

        Traveled = location.query.filter_by(soldier_id =message_dict['id']).all()#Queries table of locations using Id number of soldier and returns all entries.
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
