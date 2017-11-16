from __future__ import unicode_literals, print_function, generators, division

from view import View

__author__ = 'DIPSTER'


class ConvolutionCorrelationController:
    def index(self, params):
        status = '200 OK'
        header_view = View('views/header.html')
        body_view = View('views/index.html')
        footer_view = View('views/footer.html')
        header = header_view.render()
        body = body_view.render(messages=['one', 'two', 'three'])
        footer = footer_view.render()
        output = header + body + footer

        return status, output
