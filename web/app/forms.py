from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, FloatField, SelectField
from wtforms.validators import DataRequired, NumberRange, Length


class LoginForm(FlaskForm):
    server = StringField('Server', validators=[DataRequired()])
    dbname = StringField('Database name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Establish connection')


class WorkerForm(FlaskForm):
    fullname = StringField('Fullname', validators=[DataRequired(), Length(max=128)])
    salary = FloatField('Salary', validators=[NumberRange(min=0)])
    job = StringField('Position', validators=[Length(max=32)])
    address = StringField('Address', validators=[DataRequired(), Length(max=128)])
    passport_number = StringField('Passport number', validators=[DataRequired(), Length(max=10)])
    telephone = StringField('Telephone number', validators=[DataRequired(), Length(max=16)])
    email = StringField('Email', validators=[DataRequired(), Length(max=128)])
    submit = SubmitField('Add worker')


class SupplierForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=128)])
    address = StringField('Address', validators=[DataRequired(), Length(max=128)])
    telephone = StringField('Telephone number', validators=[DataRequired(), Length(max=16)])
    email = StringField('Email', validators=[DataRequired(), Length(max=128)])
    submit = SubmitField('Add supplier')


class CustomerForm(FlaskForm):
    fullname = StringField('Fullname', validators=[DataRequired(), Length(max=128)])
    card_id = SelectField('Card ID', coerce=int)
    address = StringField('Address', validators=[DataRequired(), Length(max=128)])
    telephone = StringField('Telephone number', validators=[DataRequired(), Length(max=16)])
    email = StringField('Email', validators=[DataRequired(), Length(max=128)])
    submit = SubmitField('Add customer')


class DiscountCardForm(FlaskForm):
    discount = FloatField('Discount', validators=[DataRequired(), NumberRange(min=0, max=1)])
    start_date = DateField('Start date', validators=[DataRequired()], default=datetime.utcnow)
    expiration = DateField('Expiration', validators=[DataRequired()])
    submit = SubmitField('Add discount card')


class ProducerForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=128)])
    address = StringField('Address', validators=[DataRequired(), Length(max=128)])
    telephone = StringField('Telephone number', validators=[DataRequired(), Length(max=16)])
    email = StringField('Email', validators=[DataRequired(), Length(max=128)])
    submit = SubmitField('Add producer')
