from collections.abc import Mapping, Sequence
from typing import Any
from flask_wtf.file import FileField, FileAllowed
from pyparsing import Regex
from GYM.models import User, Plan
from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, StringField, PasswordField, SubmitField, BooleanField, ValidationError, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp, NumberRange
from flask_login import current_user

class RegistrationForm(FlaskForm):
    username = StringField('Username*', validators= [DataRequired(), Length(min = 2, max = 20)])    
    email = StringField('Email*', validators= [DataRequired(), Email()])
    phone = StringField('Phone Number*', validators= [DataRequired(), Length(min=10, max=10), Regexp(regex='^0[0-9]{9}$', message='Invalid phone number format.')])
    password = PasswordField('Password*', validators= [DataRequired()])
    confirm_password = PasswordField('Confirm Password*', validators=  [DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a another username')
        
    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a another email')    


class LoginForm(FlaskForm):
    email = StringField('Email', validators= [DataRequired(), Email()])
    password = PasswordField('Password', validators= [DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators= [DataRequired(), Length(min = 2, max = 20)])
    phone = StringField('Contact No.', validators= [DataRequired(), Length(min=10, max=10), Regexp(regex='^0[0-9]{9}$', message='Invalid phone number format.')])
    email = StringField('Email', validators= [DataRequired(), Email()])
    current_password = PasswordField('Current Password', validators= [DataRequired()])
    new_password = PasswordField('New Password', validators= [DataRequired()])
    confirm_password = PasswordField('Re-type Password', validators= [DataRequired()])
    submit = SubmitField('Update')
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username = username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a another username')
        
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email = email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a another email')    
            
class AvailPlanForm(FlaskForm):
    username = StringField('Name of Participant', validators= [DataRequired(), Length(min = 2, max = 20)])    
    email = StringField('Email Address', validators= [DataRequired(), Email()])
    phone = StringField('Contact No.', validators= [DataRequired(), Length(min=10, max=10), Regexp(regex='^0[0-9]{9}$', message='Invalid phone number format.')])
    
    plan = SelectField('Plan', validators= [DataRequired()])
    submit = SubmitField('Avail Membership')


class AddPlanForm(FlaskForm):
    name = StringField('Plan Name', validators= [DataRequired(), Length(min = 2, max = 20)])  
    duration = IntegerField('Validity', validators= [DataRequired(), NumberRange(min=1, message='Duration must be an integer greater than 0.')])
    price = IntegerField('Price', validators= [DataRequired(), NumberRange(min=1, message='Price must be an integer greater than 0.')])    
    submit = SubmitField('Add')


class PaymentForm(FlaskForm):
    phone = StringField('Phone Number', validators= [DataRequired(), Length(min=10, max=10), Regexp(regex='^0[0-9]{9}$', message='Invalid phone number format.')])  
    plan = SelectField('Plan', validators= [DataRequired()])
    submit = SubmitField('Save')


class AddEquipmentForm(FlaskForm):
    name = StringField('Equipment Name', validators= [DataRequired(), Length(min = 2, max = 20)])  
    quantity = IntegerField('Total No.', validators= [DataRequired()])  
    submit = SubmitField('Add')


class AddCoachForm(FlaskForm):
    name = StringField('Coach Name', validators= [DataRequired(), Length(min = 2, max = 20)])  
    phone = StringField('Phone Number', validators= [DataRequired(), Length(min=10, max=10), Regexp(regex='^0[0-9]{9}$', message='Invalid phone number format.')])  
    email = StringField('Email Address', validators= [DataRequired(), Email()])
    submit = SubmitField('Add')

class UpdateCoachForm(FlaskForm):
    name = StringField('Coach Name', validators= [DataRequired(), Length(min = 2, max = 20)])  
    phone = StringField('Phone Number', validators= [DataRequired(), Length(min=10, max=10), Regexp(regex='^0[0-9]{9}$', message='Invalid phone number format.')])  
    email = StringField('Email Address', validators= [DataRequired(), Email()])
    submit = SubmitField('Update')


class UpdatePlanForm(FlaskForm):
    name = StringField('Plan Name', validators= [DataRequired(), Length(min = 2, max = 20)])  
    duration = IntegerField('Validity', validators= [DataRequired(), NumberRange(min=1, message='Duration must be an integer greater than 0.')])
    price = IntegerField('Price', validators= [DataRequired(), NumberRange(min=1, message='Price must be an integer greater than 0.')])    
    submit = SubmitField('Save')


class UpdateEquipmentForm(FlaskForm):
    name = StringField('Equipment Name', validators= [DataRequired(), Length(min = 2, max = 20)])  
    quantity = IntegerField('Total No.', validators= [DataRequired()])  
    submit = SubmitField('Save')


class RequestResetForm(FlaskForm):
    email = StringField('Email', validators= [DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')  
            

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators= [DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=  [DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')




   



    