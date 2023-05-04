import json
import tarfile

from archives_app import DeleteFiles
from archives_app.Archive import Archive


class Unpacking(Archive):
    status = 'unpacking'
    progress = 0
    files: list = []

    def __init__(self, id: int, file_path: str) -> None:
        self.id = id
        self.file_path = file_path
        self.unpack()

    def unpack(self) -> None:
        with tarfile.open(self.file_path, "r:gz") as f:
            f.extractall(self.file_path[:-7], members=self.track_progress(f), numeric_owner=True)
            self.files = f.getnames()
        self.status = 'ok'
        DeleteFiles.deleteFile(self.file_path)

    def track_progress(self, members):
        total = len(members.getmembers())
        count = 0
        for member in members:
            yield member
            count += 1
            self.progress = int(count / (total / 100))

    def get_status(self) -> str:
        log: dict
        if self.status == 'unpacking':
            log = {"status": self.status, "progress": self.progress}
        elif self.status == 'ok':
            log = {"status": self.status, "files": self.files}

        return json.dumps(log)
