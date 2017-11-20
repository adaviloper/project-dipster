import cv2

from view import View


class FirstOrderDerivateController:
    def filter(self, params):
        image_path = 'controllers/assets/images/' + params['image']

        input_image = cv2.imread(image_path, 0)

        window_size = int(params['windowSize'][0])
        print("windowSize:", window_size)
        
        sobelx = cv2.Sobel(input_image, cv2.CV_64F, 1, 0, ksize = window_size)
        sobely = cv2.Sobel(input_image, cv2.CV_64F, 0, 1, ksize = window_size)

        sobelx_output_path = 'controllers/assets/images/out/sobelx_' + params['image']
        sobely_output_path = 'controllers/assets/images/out/sobely_' + params['image']
        
        cv2.imwrite(sobelx_output_path, sobelx)
        cv2.imwrite(sobely_output_path, sobely)

        view = View()
        output = view.render(message = [sobelx_output_path, sobely_output_path])
        return '200 okay', output
