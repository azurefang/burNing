#!/usr/bin/env python

from peewee import *
from werkzeug.security import generate_password_hash, check_password_hash
from config import db
from datetime import date, datetime


class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    username = CharField(unique=True)
    password_hash = CharField()
    avatar = CharField(null=True)
    about_me = TextField(null=True)
    member_since = DateField(default=date.today())
    last_seen = DateField(default=date.today())

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verity_password(self, password):
        return check_password_hash(self.password_hash, password)

    def ping(self):
        self.last_seen = datetime.now()
        db.session.add(self)



class Node(BaseModel):
    name = CharField(unique=True)
    avatar = CharField(null=True)
    description = TextField(null=True)
    post_count = IntegerField(default=0)



class Post(BaseModel):
    user = ForeignKeyField(User, related_name='posts')
    node = ForeignKeyField(Node, related_name='posts')
    title = CharField()
    content = TextField()
    created_time = DateTimeField(default=datetime.now())
    updated_time = DateTimeField(default=datetime.now())
    hits = IntegerField(default=1)
    up_count = IntegerField(default=0)
    down_count = IntegerField(default=0)
    reply_count = IntegerField(default=0)
    last_reply_by = ForeignKeyField(User, null=True)
    last_reply_time = DateTimeField(default=datetime.now())


class Reply(BaseModel):
    post = ForeignKeyField(Post, related_name='replies')
    user = ForeignKeyField(User, related_name='replies')
    content = TextField()
    created_time = DateTimeField(default=datetime.now())
