from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField,SubmitField


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