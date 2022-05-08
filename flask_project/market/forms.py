# This form works like the SQLAlchemy models for the sqlite3 database
# To create the smart forms for beautifying and registering users, import these libraries. 
from flask_wtf import FlaskForm
from market.models import User

# The fields have to be filled inorder for the user to register for the site
# StringField, PasswordField will be the fields on the register form
from wtforms import StringField, PasswordField, SubmitField

#Now, I have to create a "validation" condition that will set limits and check for data on the fields + the password entries and check if the two fields match
#To do this, import these classes from the wtforms.validators
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError

class RegisterForm(FlaskForm):
    # what if the user's entry already exists, they would get an ugly feedback error of UNIQUE constraint failed, so to make a nice exception error, 
    # import ValidationError and from market.models import User so the validator function checks this database to see if the entry already exists
    def validate_username(self, username_to_check): # it's vital the function has the field name attached to the validate so FlaskForm in line 14 would know to check the User model according to this field
        user = User.query.filter_by(username=username_to_check.data).first() #this is saying to go check if the entered username is already in the User model (table in db)
        #remember that the sql filter will return an object, we use .first() to grab it
        if user:
            raise ValidationError('username already exists, please try a different username')
    def validate_email_address(self, email_address_to_check):
        email = User.query.filter_by(email_address=email_address_to_check.data).first() #.data to grab the data
        if email: # if there's an already existing email address
            raise ValidationError('email address already exists, pkease try a different email adress')

    #these labels show up on the spaces in the registration form
    # the validators here are connected to the page via if statement on line 73 in routes.py
    username = StringField(label='Username:', validators=[Length(min=3, max=30), DataRequired()]) #setting validator condition: username can't be less that 2 chr and more than 30 chr  
    email_address = StringField(label='E-mail:', validators=[Email(), DataRequired()])# will check for @ in email | DataRequired() will make sure there's data in the fields
    password1 = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])    # will ask for password and re-typing it for confirmation
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()]) #from line 9, this validators=...will check if password 2 and 1 match after the form is submitted
    submit = SubmitField(label='submit')

# creating form for login page
class LoginForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label='sign-in')

# for the 'Confirm purchase' line 58 in helper_tags/'buttons_modals.html', creating class for submitting confirm purchase
class PurchaseItemForm(FlaskForm):
    submit = SubmitField(label='purchase item')

# form for item sale
class SellItemForm(FlaskForm):
    submit = SubmitField(label='sell item')