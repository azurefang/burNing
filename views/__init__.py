#!/usr/bin/env python

from tornado.web import RequestHandler
import weakref
from jinja2 import Environment, FileSystemLoader
import os.path
from models import User


class BaseHandler(RequestHandler):
    _path_to_env = {}

    def login_user(self, username):
        self.set_secure_cookie("username", username)

    def current_user(self):
        username = self.get_secure_cookie("username")
        return User.select().where(User.username==username)[0]

    def get_template_path(self):
        """ 获取模板路径 """
        return '/Users/azurefang/PycharmProjects/burNing/templates'


    def create_template_loader(self, template_path):
        """ 根据template_path创建相对应的Jinja2 Environment """
        temp_path = template_path
        if isinstance(template_path, (list, tuple)):
            temp_path = template_path[0]

        env = BaseHandler._path_to_env.get(temp_path)
        if not env:
            _loader = FileSystemLoader(template_path)
            env = Environment(loader = _loader)
            BaseHandler._path_to_env[temp_path] = env
        return env


    def render_string(self, template_name, **kwargs):
        """ 使用Jinja2模板引擎 """
        env = self.create_template_loader(self.get_template_path())
        t = env.get_template(template_name)
        namespace = self.get_template_namespace()
        namespace.update(kwargs)
        return t.render(**namespace)


class TornadoFormMultiDict(object):
    """Wrapper class to provide form values to wtforms.Form

    This class is tightly coupled to a request handler, and more importantly one of our BaseHandlers
    which has a 'context'. At least if you want to use the save/load functionality.

    Some of this more difficult that it otherwise seems like it should be because of nature
    of how tornado handles it's form input.
    """
    def __init__(self, handler):
        # We keep a weakref to prevent circular references
        # This object is tightly coupled to the handler... which certainly isn't nice, but it's the
        # way it's gonna have to be for now.
        self.handler = weakref.ref(handler)

    @property
    def _arguments(self):
        return self.handler().request.arguments

    def __iter__(self):
        return iter(self._arguments)

    def __len__(self):
        return len(self._arguments)

    def __contains__(self, name):
        # We use request.arguments because get_arguments always returns a
        # value regardless of the existence of the key.
        return (name in self._arguments)

    def getlist(self, name):
        # get_arguments by default strips whitespace from the input data,
        # so we pass strip=False to stop that in case we need to validate
        # on whitespace.
        return self.handler().get_arguments(name, strip=False)

    def __getitem__(self, name):
        return self.handler().get_argument(name)
