import json
import os
import tarfile

from archives_app.Archive import Archive


class Unpacking(Archive):

    status = 'unpacking'
    progress = 0
    files = []

    def __init__(self,id: int,file_path: str):
        self.id = id
        self.file_path = file_path
        self.file_name = os.path.splitext(self.file_path)[0]
        self.unpack()

    def unpack(self):
        with tarfile.open(self.file_path) as f:

            f.extractall(self.file_path+'\\'+ self.file_name, members = self.track_progress(f))
            self.files = f.getnames()
        print(self.files)

    def track_progress(self, members):
        total = len(members)
        count = 0
        for member in members:
            yield member
            count += 1
            self.progress = int(count/(total/100))

    def get_status(self):
        log: dict
        if self.status == 'unpacking':
            log = {"status": self.status, "progress": self.progress}
        elif self.status == 'ok':
            log = {"status":self.status}

        return json.dumps(log)

