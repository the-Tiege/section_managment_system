from .extensions import db

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

    __tablename__ = 'sections'  # name of the table.

    # section number used as primary key.
    id = db.Column(db.Integer, primary_key=True)
    # total ammunition in the section.
    section_amunition = db.Column(db.Integer)
    # Number of people in the section.
    section_strength = db.Column(db.Integer)
    # Soldiers in section who are uninjured.
    section_ok = db.Column(db.Integer)
    # Soldiers in section who have become casualties.
    section_casualty = db.Column(db.Integer)
    # Location of section, Taken from section commanders location.
    section_location = db.Column(db.Text)
    # battery level indication for Section database.
    section_battery = db.Column(db.Text)
    # relationship to table soldiers.
    soldiers = db.relationship('Soldier', backref='sections', lazy='dynamic')

    def __init__(self, id, section_ammo):
        """
        Initializes a new section.

        To create the section, it requires an entry of an id number and ammunition.

        Args:
            id (int): Identifying number of the section, must be unique.
            section_ammo (int): Sections starting ammunition.
        """
        self.id = id  # Identifying number of the section must be unique.
        self.section_amunition = section_ammo  # Sections starting ammunition.


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

    __tablename__ = 'soldiers'  # Table name.

    # Army number  of soldier primary key. Must be unique.
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)  # Soldiers name.
    role = db.Column(db.Text)  # Role of section member.
    # ID number of section that soldier belongs to.
    section_id = db.Column(db.Integer, db.ForeignKey('sections.id'))
    identity_check = db.Column(db.Text)  # USed to verify soldiers identity.
    # Link  to table that  lists soldiers heart rate over time.
    vitals_history = db.relationship(
        'Vitals', backref='soldier', lazy='dynamic')
    # Link to table that lists soldiers location over times.
    location_history = db.relationship(
        'Location', backref='soldier', lazy='dynamic')
    # Stores current location of soldier.
    current_location = db.Column(db.Text)
    # Stores most recent record of soldiers location.
    last_heart_rate = db.Column(db.Integer)
    last_update_time = db.Column(db.Text)  # Stores time of last update.
    # Stores number of rounds fired by soldier.
    ammunition_expended = db.Column(db.Integer)
    # Stores battery level of Ammunition tracker.
    rifle_sensor_battery_level = db.Column(db.Text)
    status = db.Column(db.Text)  # Stores Status of soldier.
    # Stores battery level of body armour sensor.
    armour_sensor_battery_level = db.Column(db.Text)
    # Battery level of sensor hub.
    hub_sensor_battery_level = db.Column(db.Text)
    # Stores distance traveled by soldier.
    distance_traveled = db.Column(db.Text)

    def __init__(self, id, name, role, section_id):
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
        self.id = id  # Army number.
        self.name = name  # Soldiers name.
        self.role = role  # Soldiers role in the section.
        self.section_id = section_id  # Section soldier belongs to.


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

    __tablename__ = 'vitals'  # Name of table.

    # ID number of entry in database. automatically generated unique primary key.
    id = db.Column(db.Integer, primary_key=True)
    heart_rate = db.Column(db.Integer)  # Heart rate of soldier.
    update_time = db.Column(db.Text)  # Time that heart rate entry was made.
    # ID number of Soldier.
    soldier_id = db.Column(db.Integer, db.ForeignKey('soldiers.id'))
    # soldier = db.relationship('Soldier', backref='vitals_history', lazy='dynamic')

    # function used to create a new entry for heart rate for soldier.Automatically created from data sent from sensors.
    def __init__(self, heart_rate, time, soldier_id):
        """
        Initializes a new entry for heart rate for a soldier.

        Parameters:
            heart_rate (int): Heart rate.
            update_time (str): Time of the entry.
            soldier_id (int): ID number of the soldier that the entry belongs to.
        """

        self.heart_rate = heart_rate  # Heart rate.
        self.update_time = time  # Time of entry.
        # ID number of soldier that the entry belongs to.
        self.soldier_id = soldier_id


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

    __tablename__ = 'locations'  # Table name.

    # ID number of entry in database. automatically generated unique primary key.
    id = db.Column(db.Integer, primary_key=True)
    long = db.Column(db.Text)  # longitude.
    lat = db.Column(db.Text)  # latitude.
    grid_reference = db.Column(db.Text)  # Grid reference
    update_time = db.Column(db.Text)  # Time that location entry was made.
    # ID number of soldier that the entry belongs to.
    soldier_id = db.Column(db.Integer, db.ForeignKey('soldiers.id'))
    # soldier = db.relationship('Soldier', backref='location_history', lazy='dynamic')

    # function used to create a new entry for location of soldier.Automatically created from data sent from sensors.
    def __init__(self, long, lat, grid, time, soldier_id):
        """
        Initializes a new entry for the location of a soldier.

        Parameters:
            long (str): Longitude of the soldier's location.
            lat (str): Latitude of the soldier's location.
            grid_reference (str): Grid reference of the soldier's location.
            update_time (str): Time when the location entry was made.
            soldier_id (int): ID number of the soldier to whom the entry belongs.
        """
        self.long = long  # Longitude.
        self.lat = lat  # Latitude.
        self.grid_reference = grid  # Grid reference.
        self.update_time = time  # Time location entry was made.
        # ID number of soldier that the entry belongs to.
        self.soldier_id = soldier_id