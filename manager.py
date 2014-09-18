#!/usr/bin/env python3

import os.path

from tornado.options import define, options, parse_command_line
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from tornado.web import Application


define('cmd', default='runserver')
define('port', default=9000, type=int)



class App(Application):
    def __init__(self):
        from urls import routes as handlers
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__),'templates'),
            static_path=os.path.join(os.path.join(os.path.dirname(__file__),'static')),
            cookie_secret="NjAzZWY2ZTk1YWY5NGE5NmIyYWM0ZDAzOWZjMTg3YTU=|1355811811|3245286b611f74805b195a8fec1beea7234d79d6",
            login_url='/auth/login',
            xsrf_cookies= True,
            autoescape=None,
            debug=True,
            )
        Application.__init__(self, handlers, **settings)


def runserver():
    http_server = HTTPServer(App())
    http_server.listen(options.port)
    loop = IOLoop.instance()
    loop.start()

if __name__ == '__main__':
    parse_command_line()
    if options.cmd == 'runserver':
        runserver()
