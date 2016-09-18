# -*- coding: UTF-8 -*-

from flask_wtf import Form
from wtforms import PasswordField
from wtforms import BooleanField
from wtforms import StringField
from wtforms import SubmitField
from wtforms.fields.html5 import DateField
from wtforms.validators import InputRequired


class LoginForm(Form):
    username = StringField('Username', [InputRequired()])
    password = PasswordField('Password', [InputRequired()])
    login = SubmitField('Login')


class InsertForm(Form):
    text = StringField(u'Текст заметки', [InputRequired()])
    date = DateField(u'Выполнить до', format='%Y-%m-%d')
    done = BooleanField(u'Выполнено?')
    submit = SubmitField(u'Создать')
    cancel = SubmitField(u'Отмена')
