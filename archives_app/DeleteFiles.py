import json
import os
import stat
from shutil import rmtree

from archives_app.Archive import Archive


def remove_readonly(func, path, _) -> None:
    os.chmod(path, stat.S_IWRITE)
    func(path)


class DeleteFiles(Archive):
    status = 'deleted'

    def __init__(self, id: int, file_path: str) -> None:
        self.file_path = file_path
        self.id = id

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

    def get_status(self) -> str:
        log: dict
        if self.status == 'deleted':
            log = {"status": self.status}

        return json.dumps(log)
