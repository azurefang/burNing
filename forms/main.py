#!/usr/bin/env python

from forms import Form
from wtforms.fields import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class PostForm(Form):
    title = StringField('title', validators=[DataRequired()])
    content = TextAreaField('content', validators=[DataRequired()])
    submit = SubmitField('发帖')

class ReplyForm(Form):
    content = TextAreaField('context', validators=[DataRequired()])
    submit = SubmitField('回复')
