import os
import stat
from shutil import rmtree

from archives_app.Archive import Archive, dict_of_archive_names


def remove_readonly(func, path, _) -> None:
    os.chmod(path, stat.S_IWRITE)
    func(path)


class DeleteFiles(Archive):

    msg: str = None

    def __new__(cls, id: int, file_path: str):
        obj = super().__new__(cls)
        obj.file_path = file_path

        cls.deleteFile(obj.file_path)
        cls.deleteDir(obj.file_path)

        return obj

    def __init__(self, id: int, file_path: str) -> None:
        self.status = 'deleted'
        self.file_path = file_path
        self.file_name = list(dict_of_archive_names.keys())[
            list(dict_of_archive_names.values()).index(id)]
        self.id = id

        del dict_of_archive_names[self.file_name]

    def deleteDir(self) -> None:
        rmtree(self.file_path[:-7], onerror=remove_readonly)

    def deleteFile(self) -> None:
        os.remove(self.file_path)

    @staticmethod
    def deleteDir(file_path: str) -> None:
        rmtree(file_path[:-7], onerror=remove_readonly)

    @staticmethod
    def deleteFile(file_path: str) -> None:
        os.remove(file_path)

    def get_status(self) -> dict:

        log: dict
        log = {"status": self.status}
        return log
