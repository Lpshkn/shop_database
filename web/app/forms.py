from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired, NumberRange, Length


class LoginForm(FlaskForm):
    server = StringField('Server', validators=[DataRequired()])
    dbname = StringField('Database name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Establish connection')


class WorkerForm(FlaskForm):
    fullname = StringField('Fullname', validators=[DataRequired(), Length(max=128)])
    salary = IntegerField('Salary', validators=[NumberRange(min=0)])
    job = StringField('Position', validators=[Length(max=32)])
    address = StringField('Address', validators=[DataRequired(), Length(max=128)])
    passport_number = StringField('Passport number', validators=[DataRequired(), Length(max=10)])
    telephone = StringField('Telephone number', validators=[DataRequired(), Length(max=16)])
    email = StringField('Email', validators=[DataRequired(), Length(max=128)])
    submit = SubmitField('Add worker')
