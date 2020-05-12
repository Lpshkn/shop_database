import pymssql
from app import mssql
from app import app
from flask import render_template, flash, redirect, url_for, request, g
from flask_login import current_user, login_user, logout_user, login_required
from app.forms import LoginForm
from app.models import User
from werkzeug.urls import url_parse


@app.route('/login', methods=['GET', 'POST'])
def login():
    logout_user()
    mssql.close_conn()
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(username=form.username.data).first()
            if not user:
                flash('Invalid user')
                return redirect(url_for('login'))
            mssql.set_conn(
                server=form.server.data,
                user=form.username.data,
                password=form.password.data,
                dbname=form.dbname.data
            )
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('workers')
            return redirect(next_page)
        except pymssql.OperationalError:
            flash('Invalid connection data')
            return redirect(url_for('login'))
        except pymssql.InterfaceError:
            flash('Connection to the database failed for an unknown reason')
            return redirect(url_for('login'))

    return render_template('login.html', title='Sign In', form=form)


@app.route('/')
@app.route('/workers/show', methods=['GET', 'POST'])
@login_required
def workers():
    storage = mssql.WorkersStorage.get_connection(
        conn=mssql.get_conn())
    info = {
        'title': 'Workers | Shop database',
        'table_name': 'Workers',
        'link': 'workers',
        'workers': storage.get_workers()
    }
    return render_template('workers/show.html', **info)


@app.route('/suppliers/show', methods=['GET', 'POST'])
@login_required
def suppliers():
    storage = mssql.SuppliersStorage.get_connection(
        conn=mssql.get_conn())
    info = {
        'title': 'Suppliers | Shop database',
        'table_name': 'Suppliers',
        'link': 'suppliers',
        'suppliers': storage.get_suppliers()
    }
    return render_template('suppliers/show.html', **info)


@app.route('/products/show', methods=['GET', 'POST'])
@login_required
def products():
    storage = mssql.ProductsStorage.get_connection(
        conn=mssql.get_conn())
    info = {
        'title': 'Products | Shop database',
        'table_name': 'Products',
        'link': 'products',
        'products': storage.get_products()
    }
    return render_template('products/show.html', **info)


@app.route('/customers/show', methods=['GET', 'POST'])
@login_required
def customers():
    storage = mssql.CustomersStorage.get_connection(
        conn=mssql.get_conn())
    info = {
        'title': 'Customers | Shop database',
        'table_name': 'Customers',
        'link': 'customers',
        'customers': storage.get_customers()
    }
    return render_template('customers/show.html', **info)


@app.route('/discount_cards/show', methods=['GET', 'POST'])
@login_required
def discount_cards():
    storage = mssql.DiscountCardsStorage.get_connection(
        conn=mssql.get_conn())
    info = {
        'title': 'Discount cards | Shop database',
        'table_name': 'Discount cards',
        'link': 'discount_cards',
        'cards': storage.get_cards()
    }
    return render_template('discount_cards/show.html', **info)


@app.route('/producers/show', methods=['GET', 'POST'])
@login_required
def producers():
    storage = mssql.ProducersStorage.get_connection(
        conn=mssql.get_conn())
    info = {
        'title': 'Producers | Shop database',
        'table_name': 'Producers',
        'link': 'producers',
        'producers': storage.get_producers()
    }
    return render_template('producers/show.html', **info)


@app.route('/purchases/show', methods=['GET', 'POST'])
@login_required
def purchases():
    storage = mssql.PurchasesStorage.get_connection(
        conn=mssql.get_conn())
    info = {
        'title': 'Purchases | Shop database',
        'table_name': 'Purchases',
        'link': 'purchases',
        'producers': storage.get_purchases()
    }
    return render_template('purchases/show.html', **info)
