# -*- coding: UTF-8 -*-

from datetime import datetime
import functools

from flask import Flask
from flask import abort
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from flaskext.mysql import MySQL
from wtforms import Label

import forms

mysql = MySQL()
app = Flask('flask_app')
app.config.from_object('flask_app.config')
mysql.init_app(app)


@app.route('/')
def root():
    return redirect(url_for('views'))


@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    if (form.validate_on_submit() and
            form.username.data == app.config['ADMIN_USERNAME'] and
            form.password.data == app.config['ADMIN_PASSWORD']):
        session['username'] = form.username.data
        return redirect(url_for('root'))
    return render_template('login.html', form=form)


@app.route('/logout/')
def logout():
    session.pop('username', None)
    return redirect(url_for('root'))


@app.route('/search')
def search():

    db = mysql.get_db()
    cur = db.cursor()

    query = request.args.get('search')
    sql_query = u"SELECT * FROM organizer WHERE text LIKE '%{query}%';".format(query=query)
    cur.execute(sql_query)
    matches = cur.fetchall()
    time_now = datetime.now().date()

    return render_template('search.html', matches=matches, time_now=time_now)


def admin_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        username = session.get('username', None)
        if username != 'admin':
            abort(401)
        return f(*args, **kwargs)
    return decorated_function


@app.route('/insert', methods=['GET', 'POST'])
@admin_required
def insert_into_table():

    form = forms.InsertForm()

    if form.is_submitted():
        if form.cancel.data:
            return redirect(url_for('views'))
        elif form.validate():
            db = mysql.get_db()
            cur = db.cursor()
            text = form.text.data
            date = form.date.data.strftime('%Y-%m-%d')
            done = form.done.data
            sql_query = u'INSERT INTO organizer (text,date,done) VALUES ("{text}", "{date}", {done});'.format(text=unicode(text), date=str(date), done=done)
            cur.execute(sql_query)
            db.commit()

            return redirect(url_for('views'))

    return render_template('insert_values.html', form=form)


@app.route('/views/')
@admin_required
def views():
    db = mysql.get_db()
    cur = db.cursor()
    cur.execute('SELECT * FROM organizer;')
    mysql_data = cur.fetchall()
    time_now = datetime.now().date()

    return render_template('views.html', mysql_data=mysql_data, time_now=time_now)


@app.route('/edit/<int:ids>/', methods=['GET', 'POST'])
@admin_required
def edit(ids):

    sql_query = u'SELECT * FROM organizer WHERE id = {ids}'.format(ids=ids)

    db = mysql.get_db()
    cur = db.cursor()
    cur.execute(sql_query)
    mysql_data = cur.fetchall()

    form = forms.InsertForm(text=mysql_data[0][1],
                            date=mysql_data[0][2],
                            done=mysql_data[0][3])
    form.submit.label = Label('submit', u'Обновить')

    if form.is_submitted():
        if form.cancel.data:
            return redirect(url_for('views'))
        elif form.validate():
            db = mysql.get_db()
            cur = db.cursor()
            text = form.text.data
            date = form.date.data.strftime('%Y-%m-%d')
            done = form.done.data
            sql_query = u'UPDATE organizer SET text = "{text}", date = "{date}", done = {done} WHERE id = {ids};'.format(text=unicode(text), date=str(date), done=done, ids=ids)
            cur.execute(sql_query)
            db.commit()
            return redirect(url_for('views'))

    return render_template('edit.html', form=form, ids=ids)
