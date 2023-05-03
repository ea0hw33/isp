import os, stat
from shutil import rmtree

from archives_app.Archive import Archive

def remove_readonly(func, path, _):
    "Clear the readonly bit and reattempt the removal"
    os.chmod(path, stat.S_IWRITE)
    func(path)
class DeleteFiles(Archive):

    def __init__(self, file_path:str):
        self.file_path = file_path

    def deleteDir(self):
        rmtree(self.file_path[:-7],onerror= remove_readonly)

    def deleteFile(self):
        os.remove(self.file_path)

    @staticmethod
    def deleteDir(file_path:str):
        rmtree(file_path[:-7],onerror= remove_readonly)

    @staticmethod
    def deleteFile(file_path:str):
        os.remove(file_path)
