from flask_wtf import Flaskform 
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class RegistrationForm(Flaskform):
    username = StringField('username', validators=[DataRequired(), Length(min=3, max=15)])
    email = StringField('email', validators=[DataRequired(), Length(min=3, max=15), Email()])
    password  = PasswordField('password', validators=[DataRequired(), Length(min=6, max=12)])
    confirm_password = PasswordField('confirm_password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(Flaskform):
    email = StringField('email', validators=[DataRequired(), Length(min=3, max=15), Email()])
    password  = PasswordField('password', validators=[DataRequired(), Length(min=6, max=12)])
    submit = SubmitField('Register')