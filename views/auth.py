#!/usr/bin/env python

from views import BaseHandler
from models import *
from forms.auth import *
from views import TornadoFormMultiDict



class RegisterHandler(BaseHandler):
    def get(self):
        form = RegistrationForm()
        self.render('auth/register.html', form=form)

    def post(self):
        form = RegistrationForm(TornadoFormMultiDict(self))
        if form.validate():
            username = self.get_argument("username")
            password = self.get_argument("password")
            user = User(username = username, password=password)
            user.save()
            self.redirect('/auth/login')
        else:
            self.render('auth/register.html', form=form)



class LoginHandler(BaseHandler):
    def get(self):
        form = LoginForm()
        self.render('auth/login.html', form=form)

    def post(self):
        username = self.get_argument('username')
        password = self.get_argument('password')
        user = User.select().where(User.username==username)[0]
        if user is not None and user.verity_password(password):
            self.login_user(username)
            self.redirect('/')
        else:
            self.redirect('/auth/login')
