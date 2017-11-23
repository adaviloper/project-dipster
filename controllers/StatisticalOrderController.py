import cv2
import numpy as np
import math
from skimage.exposure import rescale_intensity
from view import View
# from controllers.ConvolutionController import ConvolutionController as conv

class StatisticalOrderController:
    def filter(self, params):
        image_path = 'controllers/assets/images/' + params['image']
        windowsize = params['windowSize']
        windowsize = int(windowsize[-1])
        filtertype = params['statisticalFilter']
        print(filtertype)

        input_image = cv2.imread(image_path, 0)
        a = StatisticalOrderController()
        # add noise
        if params['image']=='gaussian_noise.png':
            out_img1 = a.add_gaussian_noise(input_image, 40)
        elif params['image'] == 'saltandpepper_noise.png':
            out_img1 = a.add_saltandpepper_noise(input_image, 7)
        else:
            out_img1 = a.add_saltandpepper_noise(input_image, 7)

        # filter

        if filtertype == 'mean':
            out_img2 = a.mean_filtering(out_img1, windowsize)
        elif filtertype == 'median':
            out_img2 = a.median_filtering(out_img1, windowsize)
        elif filtertype == 'adaptive':
            out_img2 = a.adaptive_filter(out_img1, windowsize)

        image_output1_path = 'controllers/assets/images/out/1_' + params['image']
        image_output2_path = 'controllers/assets/images/out/2_' +  params['statisticalFilter']+params['windowSize']+params['image']
        cv2.imwrite(image_output1_path, out_img1)
        cv2.imwrite(image_output2_path, out_img2)
      
        ssim = a.ssim(input_image, out_img2)
        output_str2 = image_output2_path + '?ssim=' + str(ssim)
        # print(str)
        view = View()
        output = view.render(message=[image_output1_path, output_str2])

        return '200 okay', output

    def img_padding(self, img, size, num):
        size = int(size)
        x, y = np.shape(img)
        m = int(x + 2 * size)
        n = int(y + 2 * size)
        padd = num * np.ones((m, n), np.int)
        for i in range(size, x + size):
            for j in range(size, y + size):
                padd[i, j] = img[i - size, j - size]
        return padd

    def img_cropping(self, padded_img, size):
        x, y = np.shape(padded_img)
        m = x - 2 * size
        n = y - 2 * size
        img = np.zeros((m, n))
        for i in range(0, m):
            for j in range(0, n):
                img[i, j] = padded_img[i + size, j + size]
        return img

    def median_filtering(self, img, window_size):
        # window size must be odd>=3
        x, y = np.shape(img)
        new_img = np.zeros((x, y))
        size = int((window_size - 1) / 2)
        padded_img = self.img_padding(img, size, 0)
        for i in range(size, x + size):
            for j in range(size, y + size):
                l = []
                for m in range(-1 * size, size + 1):
                    for n in range(-1 * size, size + 1):
                        l.append(padded_img[i + m, j + n])
                new_img[i - size, j - size] = np.median(l)
        new_img = new_img.astype(np.uint8)
        return new_img

    def mean_filtering(self, img, window_size):
        # window size must be odd>=3
        x, y = np.shape(img)
        new_img = np.zeros((x, y))
        size = int((window_size - 1) / 2)
        padded_img = self.img_padding(img, size, 0)
        for i in range(size, x + size):
            for j in range(size, y + size):
                l = []
                for m in range(-1 * size, size + 1):
                    for n in range(-1 * size, size + 1):
                        l.append(padded_img[i + m, j + n])
                new_img[i - size, j - size] = np.mean(l)

        new_img = new_img.astype(np.uint8)
        return new_img
    def adaptive_filter(self,img,window_size):
        x, y = np.shape(img)
        new_img = np.zeros((x, y))
        ns=[]
        for i in range(0,50):
            for j in range(0,100):
                ns.append(img[i,j])
        vn=np.var(ns)
        size = int((window_size - 1) / 2)
        padded_img = self.img_padding(img, size, 0)
        for i in range(size, x + size):
            for j in range(size, y + size):
                l = []
                for m in range(-1 * size, size + 1):
                    for n in range(-1 * size, size + 1):
                        l.append(padded_img[i + m, j + n])
                vl=np.var(l)+1

                ml=np.mean(l)
                new_img[i - size, j - size] = padded_img[i,j] - (vn/vl)*(padded_img[i,j]-ml)
        new_img = new_img.astype(np.uint8)
        return new_img
    def ssim(self, img1, img2):
        l1 = []
        l2 = []
        print(img1.shape)
        print(img2.shape)
        for i in range(0, np.shape(img1)[0]):
            for j in range(0, np.shape(img1)[1]):
                l1.append(img1[i, j])
                l2.append(img2[i, j])
        u1 = np.mean(l1)
        u2 = np.mean(l2)
        s1 = np.std(l1)
        s2 = np.std(l2)
        cov = np.cov(l1, l2)[0, 1]
        c1 = (0.01 * 255) ** 2
        c2 = (0.03 * 255) ** 2
        c3 = c2 / 2
        LL = (2 * u1 * u2 + c1) / (u1 ** 2 + u2 ** 2 + c1)
        CC = (2 * s1 * s2 + c2) / (s1 ** 2 + s2 ** 2 + c2)

        SS = abs(np.corrcoef(l1, l2)[0, 1])

        ssim = SS * LL * CC

        return ssim

    def create_testimg(self, n):
        # this is used to create img for testing with a size n*n
        img = np.zeros((n, n))
        for i in range(0, n):
            for j in range(0, n):
                img[i, j] = 80
        for i in range(int(n / 4), 3 * int(n / 4)):
            for j in range(int(n / 4), 3 * int(n / 4)):
                img[i, j] = 160
        r = int(n / 6)
        for i in range(0, n):
            for j in range(0, n):
                d = (i - (n / 2)) ** 2 + (j - (n / 2)) ** 2
                if d < r ** 2:
                    img[i, j] = 230
        img = img.astype(np.uint8)
        return img

    def add_gaussian_noise(self, img, sigma):
        new_img = img.copy()
        for i in range(0, np.shape(img)[0]):
            for j in range(0, np.shape(img)[1]):
                new_img[i, j] = np.random.normal(img[i, j], sigma)
                new_img[i, j] = int(new_img[i, j])

        new_img = new_img.astype(np.uint8)
        return new_img

    def add_saltandpepper_noise(self, img, p):
        new_img = img.copy()
        for i in range(0, np.shape(img)[0]):
            for j in range(0, np.shape(img)[1]):
                t1 = np.random.uniform(0, 10)
                if t1 > p:
                    t2 = int(np.random.uniform(0, 10))
                    if t2 % 2 == 0:
                        new_img[i, j] = 0

                    else:
                        new_img[i, j] = 255

        new_img = new_img.astype(np.uint8)
        return new_img
