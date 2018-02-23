# coding: utf-8
class WrongFilePath(BaseException):
    def __init__(self, wrong_file_path=""):
        self.wrong_file_path = wrong_file_path

    def __str__(self):
        return "File {} does not exist.".format(self.wrong_file_path)