from flask_wtf import FlaskForm
from wtforms import SelectField, TextAreaField, StringField, HiddenField
from wtforms.validators import DataRequired

from app.ext.database import db
from app.ext.database.models import *


class FormFiltroTabelas():
    pass