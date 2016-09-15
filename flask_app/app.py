import functools

from flask import Flask
from flask import abort
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
import forms

app = Flask('flask_app')
app.config.from_object('flask_app.config')


@app.route('/')
def root():
    return render_template('base.html')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    # TODO: Convenient redirect.
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
    # TODO: Validation error handling.
    return render_template('admin.html')
