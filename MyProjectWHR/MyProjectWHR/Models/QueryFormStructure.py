
### ----------------------------------------------------------- ###
### --- include all software packages and libraries needed ---- ###
### ----------------------------------------------------------- ###

from datetime  import datetime
from flask_wtf import FlaskForm
from wtforms   import StringField, SubmitField
from wtforms   import Form, BooleanField, PasswordField, IntegerField, SelectField, SelectMultipleField
from wtforms   import TextField, TextAreaField, SelectField
from wtforms   import validators, ValidationError

from wtforms.fields.html5 import DateField
from wtforms.validators   import DataRequired

# -------------------------------------------------------
# Query form
# -------------------------------------------------------
class QueryFormStructure(FlaskForm):
    measures_mselect = SelectMultipleField('Select Measures:')
    country_mselect = SelectMultipleField('Select Countries:' , validators = [DataRequired] )
    year = SelectField('Select Year: ', choices = [('2016', '2016'),('2018', '2018'),('2019', '2019')])
    submit = SubmitField('Submit')

# -------------------------------------------------------
# Registration and login form
# -------------------------------------------------------
class LoginFormStructure(FlaskForm):
    username   = StringField('User name:  ' , validators = [DataRequired()])
    password   = PasswordField('Pass word:  ' , validators = [DataRequired()])
    submit = SubmitField('Submit')

class UserRegistrationFormStructure(FlaskForm):
    FirstName  = StringField('First name:  ' , validators = [DataRequired()])
    LastName   = StringField('Last name:  ' , validators = [DataRequired()])
    PhoneNum   = IntegerField('Phone number:  ' , validators = [DataRequired()])
    EmailAddr  = StringField('E-Mail:  ' , validators = [DataRequired()])
    username   = StringField('User name:  ' , validators = [DataRequired()])
    password   = PasswordField('Pass word:  ' , validators = [DataRequired()])
    submit = SubmitField('Submit')



