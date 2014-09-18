from peewee import SqliteDatabase

db = SqliteDatabase('main.db')

POSTS_PAGINATION = 15
REPLIES_PAGINATION = 15