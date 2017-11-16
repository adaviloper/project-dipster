from view import View


class ImagesController:
    def get_image(self, params):
        image = View('assets/images/dog.png').render()
        return '200 okay', image
