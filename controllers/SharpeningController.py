from view import View


class SharpeningController:
    def sharpen(self, request_method, get, post):
        print("sharpening method called again")
        view = View('views/sharpening.html')
        header = View('views/header.html').render()
        body = view.render()
        footer = View('views/footer.html').render()
        content = header + body + footer

        print(type(body))
        return "200 okay", content

    def test(self, params):
        image_path = 'hello world'
        # use 'empty' for dumping the output parameter to the page
        view = View('views/empty.html')
        output = view.render(message=[image_path])
        return "200 okay", output
