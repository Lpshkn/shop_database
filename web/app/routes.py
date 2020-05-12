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
        'table_name': 'workers',
        'workers': storage.get_workers()
    }
    return render_template('workers/show.html', **info)


@app.route('/suppliers/show', methods=['GET', 'POST'])
@login_required
def suppliers():

    info = {
        'title': 'Suppliers | Shop database',
        'table_name': 'workers'
    }
    return render_template('suppliers.html', **info)

