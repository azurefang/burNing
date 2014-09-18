#!/user/bin/env python

from views.auth import *
from views.main import *


routes = [
    (r'/', IndexHandler),
	(r'/auth/register', RegisterHandler),
	(r'/auth/login', LoginHandler),
    (r'/node/(\w+)$', NodeHandler),
    (r'/post/(\d+)$', PostHandler),
    (r'/user/(\w+)$', ProfileHandler),
]
