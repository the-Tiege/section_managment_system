from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField,SubmitField

#Forms to take input from user.

#The following classes can be sent to a html page to recieve data from the user.
#When the AddForm is sent to the html page for example, when getting the id of the soldier 'id = IntegerField('Service No : ')'
#id is the variable that is returned to the server and 'Service No:' is the label displayed to the user.
#Information gathered using the forms is returned when the submit button is pressed.

class AddForm(FlaskForm):
    """
    Form used to add a member to the section.

    Attributes:
    - id (IntegerField): Stores Army number to be sent to the server.
    - name (StringField): Stores the name to be sent to the server.
    - section_id (IntegerField): Stores Section number to be sent to the server.
    - role (SelectField): Displays a list of different choices for the role of a section member.
    - submit (SubmitField): Submits the form when the button is pressed.
    """

    id = IntegerField('Service No : ')#Stores Army number to be sent to server.
    name = StringField('Name : ')##Stores name to be sent to server.
    section_id = IntegerField('Section No : ')#Stores Section number to be sent to server.
    #displays a list of different choices for the role of a section member.
    role = SelectField("Role : ", choices=[("I/C", "I/C"),("2I/C","2I/C"),("1 Scout","1 Scout"),("2 Scout","2 Scout"),
                        ("3 Rifleman","3 Rifleman"),("4 Rifleman","4 Rifleman"),("5 Rifleman","5 Rifleman"),
                        ("6 Rifleman","6 Rifleman"),("7 Rifleman","7 Rifleman"),("8 Rifleman","8 Rifleman"),("1 FSG","1 FSG"),("2 FSG","2 FSG")])
    submit = SubmitField('Add to Section ')#Submits form when button pressed.

class DelForm(FlaskForm):
    """
    Form used to remove a section member.

    Attributes:
    - id (IntegerField): Stores Army number to be sent to the server.
    - submit (SubmitField): Submits the form when the button is pressed.
    """

    id = IntegerField('Service Number : ')#Stores Army number to be sent to server.
    submit = SubmitField('Remove from Section')#Submits form when button pressed


class CreateSection(FlaskForm):
    """
    Form used to create a new section.

    Attributes:
    - id (IntegerField): Stores Section number to be sent to the server.
    - SectionAmmo (IntegerField): Stores the amount of ammunition the section has on creation.
    - submit (SubmitField): Submits the form when the button is pressed.
    """

    id = IntegerField('Section Number : ')#Stores Section number to be sent to server.
    SectionAmmo = IntegerField('Amunition : ')#Stores ammount of ammunition section has on creation.
    submit = SubmitField('Create Section ')#Submits form when button pressed.

class Addammo(FlaskForm):
    """
    Form used to add ammunition to the section.

    Attributes:
    - id (IntegerField): Stores Section number to be sent to the server.
    - SectionAmmo (IntegerField): Stores the amount of ammunition to be added.
    - submit (SubmitField): Submits the form when the button is pressed.
    """

    id = IntegerField('Section Number : ')#Stores Section number to be sent to server.
    SectionAmmo = IntegerField('Amunition : ')#Stores ammount of ammunition section has on creation.
    submit = SubmitField('Add Amunition')#Submits form when button pressed.


class DelSection(FlaskForm):
    """
    Form used to delete an entire section.

    Attributes:
    - id (IntegerField): Stores Section number to be sent to the server.
    - submit (SubmitField): Submits the form when the button is pressed.
    """

    id = IntegerField('Section Number : ')#Stores Section number to be sent to server.
    submit = SubmitField('Remove Section')#Submits form when button pressed.

class HeartForm(FlaskForm):
    """
    Form used to select a soldier to display a list of their heart rate at different times.

    Attributes:
    - id (IntegerField): Stores Army number to be sent to the server.
    - submit (SubmitField): Submits the form when the button is pressed.
    """

    id = IntegerField('ID number : ')#Stores Army number to be sent to server.
    submit = SubmitField('View')#Submits form when button pressed.

class LocationForm(FlaskForm):
    """
    Form used to select a soldier to display a list of their location at different times.

    Attributes:
    - id (IntegerField): Stores Army number to be sent to the server.
    - submit (SubmitField): Submits the form when the button is pressed.
    """

    id = IntegerField('ID number : ')#Stores Army number to be sent to server.
    submit = SubmitField('View')#Submits form when button pressed.
