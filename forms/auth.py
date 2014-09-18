#!/usr/bin/env python

from wtforms.fields import  StringField, SubmitField, PasswordField, BooleanField
from forms import Form
from wtforms.validators import EqualTo, DataRequired


class RegistrationForm(Form):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired(), EqualTo('password2', message='密码不匹配')])
    password2 = PasswordField('password2', validators=[DataRequired()])
    submit = SubmitField('注册')


class LoginForm(Form):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('keep me logged in')
    submit = SubmitField('登录')
