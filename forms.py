from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, BooleanField
from wtforms.fields.html5 import URLField, IntegerField
from wtforms.validators import NumberRange, InputRequired

class AddPetForm(FlaskForm):

    name = StringField("Pet Name", validators=[InputRequired()])
    species = SelectField("Species", validators=[InputRequired()], choices=[("cat", "cat"), ("dog", "dog"), ("porcupine", "porcupine")])
    photo_url = URLField("Photo URL")
    age = IntegerField("Age", validators=[NumberRange(min=0, max=30)])
    notes = TextAreaField("Notes")
    

class EditPetForm(AddPetForm):

    available = BooleanField("Available")