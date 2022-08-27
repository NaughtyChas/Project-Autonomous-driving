import cv2
from matplotlib import pyplot as plt
import os

if __name__ == '__main__':
    path = "Raspberry/photos/rawphotos"
    datanames = os.listdir(path)
    for i in datanames:
        image = cv2.imread('photos/rawphotos/i')
        cv2.imwrite(i + 'raw.jpg', image)

        height, width, _ = image.shape
        print(f"height = {height}, width = {width}")

        left_top_image = image[:height // 2, :width // 2, :]
        cv2.imwrite("photos/1_left_top.jpg", left_top_image)

        dst = cv2.fastNlMeansDenoisingColored(image, None, 30, 30, 7, 21)
        plt.subplot(121), plt.imshow(image)
        plt.subplot(122), plt.imshow(dst)
        plt.show()
        cv2.imwrite("photos/1_gaussblur.jpg", dst)

        black_white_image = cv2.cvtColor(dst, cv2.COLOR_RGB2GRAY)
        cv2.imwrite("photos/2_black_white.jpg", black_white_image)
        print(f"image shape = {image.shape}"
              f"black_white image shape = {black_white_image.shape}\n")

        for thresh in range(5, 9):
            ret, thresh_image = cv2.threshold(black_white_image, 100, 255, cv2.THRESH_BINARY)
            cv2.imwrite(f"photos/3_thresh-{thresh}.jpg", thresh_image)

        clean_image = cv2.dilate(thresh_image, (300, 300), iterations=10)
        clean_image = cv2.threshold(clean_image, thresh, 255, cv2.THRESH_BINARY)
        clean_image = cv2.erode(thresh_image, (300, 300), iterations=10)
        clean_image[:height // 3, :] = 0
        cv2.imwrite(i + "photos/clean.jpg", clean_image)
