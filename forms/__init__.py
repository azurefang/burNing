#!/usr/bin/env python

from wtforms import Form as BaseForm


class Form(BaseForm):

    class Meta:
        locales = ['zh_CN', 'zh']
