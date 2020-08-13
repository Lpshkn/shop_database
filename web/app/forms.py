from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import (
    StringField, DateField, PasswordField, SubmitField, DateTimeField, FloatField, SelectField, IntegerField)
from wtforms.validators import (
    DataRequired, NumberRange, Length, Regexp)


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
    passport_number = StringField('Passport number', validators=[DataRequired(), Length(max=10), Regexp('^[\d]+$')])
    telephone = StringField('Telephone number', validators=[DataRequired(), Length(max=16), Regexp('^[\d()-]+$')])
    email = StringField('Email', validators=[DataRequired(), Length(max=128), Regexp('^[\w@.]+$')])
    submit = SubmitField('Add worker')


class SupplierForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=128)])
    address = StringField('Address', validators=[DataRequired(), Length(max=128)])
    telephone = StringField('Telephone number', validators=[DataRequired(), Length(max=16)])
    email = StringField('Email', validators=[DataRequired(), Length(max=128), Regexp('^[\w@.]+$')])
    submit = SubmitField('Add supplier')


class CustomerForm(FlaskForm):
    fullname = StringField('Fullname', validators=[DataRequired(), Length(max=128)])
    card_id = SelectField('Card ID', coerce=int)
    address = StringField('Address', validators=[DataRequired(), Length(max=128)])
    telephone = StringField('Telephone number', validators=[DataRequired(), Length(max=16), Regexp('^[\d()-]+$')])
    email = StringField('Email', validators=[DataRequired(), Length(max=128), Regexp('^[\w@.]+$')])
    submit = SubmitField()


class DiscountCardForm(FlaskForm):
    discount = FloatField('Discount', validators=[DataRequired(), NumberRange(min=0, max=1)])
    start_date = DateField('Start date', validators=[DataRequired()], default=datetime.utcnow)
    expiration = DateField('Expiration', validators=[DataRequired()])
    submit = SubmitField('Add discount card')


class ProductForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=128)])
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=1, max=32767)], default=1)
    price = FloatField('Price', validators=[DataRequired(), NumberRange(min=0)], default=0)
    promotion = StringField('Promotion', validators=[Length(max=30), Regexp('^[0-9+%-]+$')])
    producer = SelectField('Producer', coerce=int)
    supplier = SelectField('Supplier', coerce=int)
    submit = SubmitField('Add product')


class ProducerForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=128)])
    address = StringField('Address', validators=[DataRequired(), Length(max=128)])
    telephone = StringField('Telephone number', validators=[DataRequired(), Length(max=16), Regexp('^[\d()-]+$')])
    email = StringField('Email', validators=[DataRequired(), Length(max=128), Regexp('^[\w@.]+$')])
    submit = SubmitField('Add producer')


class PurchaseForm(FlaskForm):
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=1, max=32767)], default=1)
    total_cost = FloatField('Total cost', validators=[DataRequired(), NumberRange(min=0)], default=0)
    date = DateTimeField('Date', validators=[DataRequired()], default=datetime.utcnow)
    product_id = SelectField('Product ID', coerce=int)
    worker_id = SelectField('Worker ID', coerce=int)
    customer_id = SelectField('Customer ID', coerce=int)
    submit = SubmitField('Add purchase')
