from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, TextAreaField,DateField, FloatField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange, ValidationError, Optional
from expiry_app.models import Users
from flask_login import current_user


class RegistrationForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    role = StringField('Role', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired(), Length(min=2,max=100)])
    contact_number = StringField('Contact_number',validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_username(self, name):
        user = Users.query.filter_by(name=name.data).first()
        if user:
            raise ValidationError('Please use a different username.')
    
    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Please use a different email address.')
    
    def validate_role(self,role):
        if role.data not in ['Store','Organization']:
            raise ValidationError('The role has to be "Store" or "Organization"')
        

# class StoreForm(FlaskForm):
#     name = StringField('Name', validators=[DataRequired(), Length(min=2,max=100)])
#     location = StringField('Location', validators=[DataRequired()])
#     contact_number = StringField('Contact_number',validators=[DataRequired()])
#     submit = SubmitField('Submit')


class InventoryForm(FlaskForm):
    name = StringField('Name',validators=[DataRequired()])
    category = StringField('Type',validators=[DataRequired()])
    expiry_date = DateField('Expiry Date',validators=[DataRequired()])
    quantity = IntegerField('Quantity',validators=[DataRequired()])
    desc = StringField('Description',validators=[DataRequired()])
    brand = StringField('Brand',validators=[DataRequired()])
    submit = SubmitField('Submit')

                                 


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
