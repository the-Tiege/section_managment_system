from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField

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