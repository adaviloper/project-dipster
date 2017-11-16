from wsgiref.simple_server import make_server

import wsgi

PORT = 8080

print("Open: http://127.0.0.1:{0}/".format(PORT))
httpd = make_server('localhost', PORT, wsgi.application)
httpd.serve_forever()
