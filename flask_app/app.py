import functools

from flask import Flask
from flask import abort
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from flaskext.mysql import MySQL
import forms

mysql = MySQL()
app = Flask('flask_app')
app.config.from_object('flask_app.config')
mysql.init_app(app)


@app.route('/')
def root():
    return render_template('base.html')


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
    query = request.args.get('search')
    matches = {}
    return render_template('search.html', matches=matches)


def admin_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        username = session.get('username', None)
        if username != 'admin':
            abort(401)
        return f(*args, **kwargs)
    return decorated_function


@app.route('/admin/')
@admin_required
def admin():
    return render_template('admin.html')


@app.route('/admin/insert', methods=['GET', 'POST'])
@admin_required
def insert_into_table():

    form = forms.InsertForm()

    if form.is_submitted():
        if form.cancel.data:
            return redirect(url_for('admin'))
        elif form.validate():
            cur = mysql.get_db().cursor()
            text = form.text.data
            print text
            date = form.date.data.strftime('%Y-%m-%d')
            done = form.done.data
            sql_query = 'INSERT INTO organizer (text,date,done) VALUES ("{text}", "{date}", {done})'.format(text=str(text), date=str(date), done=done)
            cur.execute(sql_query)

            return redirect(url_for('admin'))

    return render_template('insert_values.html', form=form)
