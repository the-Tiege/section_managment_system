from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField

class LocationForm(FlaskForm):
    """
    Form used to select a soldier to display a list of their location at different times.

    Attributes:
    - id (IntegerField): Stores Army number to be sent to the server.
    - submit (SubmitField): Submits the form when the button is pressed.
    """

    id = IntegerField('ID number : ')#Stores Army number to be sent to server.
    submit = SubmitField('View')#Submits form when button pressed.