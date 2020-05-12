import pymssql
from app import app
from flask import render_template, flash, redirect, url_for, request, g
from flask_login import current_user, login_user, logout_user, login_required
from app.forms import LoginForm
from app.models import User
from app.mssql import get_db, set_db, close_db
from werkzeug.urls import url_parse


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    cursor = get_db().cursor()
    cursor.execute("SELECT * FROM shopdb.dbo.Workers")
    row = list(cursor.fetchone())
    info = {
        'user': 'User',
        'info': row
    }
    return render_template('index.html', **info)


@app.route('/login', methods=['GET', 'POST'])
def login():
    logout_user()
    close_db()
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(username=form.username.data).first()
            if not user:
                flash('Invalid user')
                return redirect(url_for('login'))

            set_db(
                server=form.server.data,
                user=form.username.data,
                password=form.password.data,
                dbname=form.dbname.data
            )
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('index')
            return redirect(next_page)
        except pymssql.OperationalError:
            flash('Invalid connection data')
            return redirect(url_for('login'))
        except pymssql.InterfaceError:
            flash('Connection to the database failed for an unknown reason')
            return redirect(url_for('login'))

    return render_template('login.html', title='Sign In', form=form)
