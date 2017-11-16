from __future__ import unicode_literals, print_function, generators, division
from pathlib import Path
from controllers import *


__author__ = 'DIPSTER'


class Router:
    def __init__(self):
        self._routes = {
            "GET": {},
            "POST": {}
        }

    def get(self, url, controller_method):
        url = url.strip('/')
        self._routes['GET'][url] = controller_method

    def post(self, url, controller_method):
        url = url.strip('/')
        self._routes['POST'][url] = controller_method

    def resolve(self, request_method, url):
        url = url.strip('/')
        if url in self._routes[request_method]:
            controller, method = self._routes[request_method][url].split('@')
            controller = eval(controller)
            callback = getattr(controller, method)
            if callback:
                return callback
        elif Path(url).is_file():
            print("file exists")

        else:
            print('not in routes')
        return self.default_controller

    def default_controller(self, *args, **kwargs):
        status = '200 OK'
        body = b''
        return status, body
