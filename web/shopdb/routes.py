from shopdb import app
from flask import render_template, flash, redirect, url_for
from shopdb.forms import LoginForm


@app.route('/')
@app.route('/index')
def index():
    info = {
        'user': 'User'
    }
    return render_template('index.html', **info)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user %s, remember me=%s' % (form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)
