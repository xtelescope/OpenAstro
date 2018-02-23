# coding: utf-8
import os
import cv2
from astropy.io import fits
from .exceptions import WrongFilePath


class Image:
    def __init__(self, directory="", image_name=None):
        self.image_path = os.path.join(directory, image_name)
        self.image_data = self.init_image_data()

    def init_image_data(self):
        if os.path.exists(self.image_path):
            with fits.open(self.image_path) as fit:
                self.image_data = fit[0].data
            return self.image_data
        else:
            raise WrongFilePath(self.image_path)

    def bayer_to_rgb(self, bayer_pattern=None):
        """

        :param bayer_pattern:
        :return:
        """
        bayer_pattern = bayer_pattern.lower()
        method = None
        if bayer_pattern == "bggr":
            method = cv2.COLOR_BAYER_BG2RGB
        elif bayer_pattern == "rggb":
            method = cv2.COLOR_BAYER_RG2RGB
        elif bayer_pattern == "gbrg":
            method = cv2.COLOR_BAYER_GB2RGB
        elif bayer_pattern == "grbg":
            method = cv2.COLOR_BAYER_GR2RGB
        if method:
            self.image_data = cv2.cvtColor(self.image_data, method)

        return self

    def center_crop(self, width=640, height=480):
        try:
            (h, w, _) = self.image_data.shape
        except Exception as e:
            (h, w) = self.image_data.shape
        x, y = int(h/2), int(w/2)
        print(h, w, x, y)
        self.image_data = self.image_data[x-int(height/2):x+int(height/2), y-int(width/2):y+int(width/2)]
        return self

    def resize(self, width=None, height=None, percentage=None):
        if percentage is None:
            self.image_data = cv2.resize(self.image_data, (int(width), int(height)))
        else:
            try:
                (height, width, _) = self.image_data.shape
            except Exception as e:
                (height, width) = self.image_data.shape
            self.image_data = cv2.resize(self.image_data, (int(width * percentage), int(height * percentage)))

        return self

    def save_to(self, directory="", image_name=""):
        image_path = os.path.join(directory, image_name)
        cv2.imwrite(image_path, self.image_data)