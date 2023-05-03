import json
import requests
from archives_app.Archive import Archive
from archives_app import app
from archives_app.Unpacking import Unpacking

list_of_archive = []

class Downloader(Archive):

    progress = 0
    status = "downloading"

    def __init__(self, link: str, id: int):
        self.id = id
        self.link = link
        self.file = self.link[self.link.rfind('/') + 1:]
        self.file_path = app.config['DATASAVE_PATH'] + self.file
        list_of_archive.append(self)
        self.download_archive()


    def download_archive(self):
        with open(self.file_path, "wb") as f:
            response = requests.get(self.link, stream=True)
            total_length = response.headers.get('content-length')

            if total_length is None:
                f.write(response.content)
            else:
                dl = 0
                total_length = int(total_length)
                for data in response.iter_content(chunk_size=4096):
                    f.write(data)
                    dl += len(data)
                    self.progress = int(dl / (total_length / 100))
        del self

    def get_status(self):
        log: dict
        if self.status == 'downloading':
            log = {"status": self.status, "progress": self.progress}

        return json.dumps(log)

    def __del__(self):
        # print('2')
        list_of_archive[self.id - 1] = Unpacking(self.id, file_path=self.file_path)