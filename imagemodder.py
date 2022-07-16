import cv2
import numpy as np


class ImageArrMod:
    def __init__(self, cv2_src):
        self.__orig_cv2_src = cv2_src
        self.__cv2_src = self.__orig_cv2_src.copy()
        #print(self.__cv2_src.shape)

    def get_image_arr(self):
        return self.__cv2_src

    def restore_image_arr(self):
        self.__cv2_src = self.__orig_cv2_src.copy()

    # Shifts the hue of an image by the specified amount
    def hue_shift_image_arr(self, amount):
        # Create a new array of the same size as the original
        new_arr = np.zeros(self.__cv2_src.shape, np.uint8)
        hsv = cv2.cvtColor(self.__cv2_src, cv2.COLOR_BGR2HSV)
        # For each pixel in the original array, shift the hue by the specified amount
        for i in range(hsv.shape[0]):
            for j in range(hsv.shape[1]):
                #print(self.__cv2_src[i, j])
                if self.__orig_cv2_src[i, j][0] != 255 or self.__orig_cv2_src[i, j][1] != 0 or self.__orig_cv2_src[i, j][2] != 255:
                    hsv[i, j, 0] = (hsv[i, j, 0] + amount) % 180
                    new_arr[i, j] = hsv[i, j]
                else:
                    new_arr[i, j] = self.__orig_cv2_src[i, j]
        self.__cv2_src = cv2.cvtColor(new_arr, cv2.COLOR_HSV2BGR)

    # Shifts the opacity of an image by the specified amount
    def opacity_shift_image_arr(self, amount):
        # Create a new array of the same size as the original
        new_arr = np.zeros(self.__cv2_src.shape, np.uint8)
        # For each pixel in the original array, shift the opacity by the specified amount
        for i in range(self.__cv2_src.shape[0]):
            for j in range(self.__cv2_src.shape[1]):
                new_arr[i, j] = self.__cv2_src[i, j]
                new_arr[i, j][3] = (new_arr[i, j][3] + amount) % 255
        self.__cv2_src = new_arr

    # Shifts the saturation of an image by the specified amount
    def saturation_shift_image_arr(self, amount):
        # Create a new array of the same size as the original
        new_arr = np.zeros(self.__cv2_src.shape, np.uint8)
        # For each pixel in the original array, shift the saturation by the specified amount
        for i in range(self.__cv2_src.shape[0]):
            for j in range(self.__cv2_src.shape[1]):
                hsv = cv2.cvtColor(self.__cv2_src[i, j], cv2.COLOR_BGR2HSV)
                hsv[1] = (hsv[1] + amount) % 255
                new_arr[i, j] = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        self.__cv2_src = new_arr

    # Shifts the brightness of an image by the specified amount
    def brightness_shift_image_arr(self, amount):
        # Create a new array of the same size as the original
        new_arr = np.zeros(self.__cv2_src.shape, np.uint8)
        # For each pixel in the original array, shift the brightness by the specified amount
        for i in range(self.__cv2_src.shape[0]):
            for j in range(self.__cv2_src.shape[1]):
                hsv = cv2.cvtColor(self.__cv2_src[i, j], cv2.COLOR_BGR2HSV)
                hsv[2] = (hsv[2] + amount) % 255
                new_arr[i, j] = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        self.__cv2_src = new_arr
