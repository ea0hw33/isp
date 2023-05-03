import json
import requests
from archives_app.Archive import Archive
from archives_app import app

list_of_archive = []

class Downloader(Archive):

    progress = 0
    status = "downloading"

    def __init__(self, link: str, id: int):
        self.id = id
        self.link = link
        self.file_name = self.link[self.link.rfind('/') + 1:]
        list_of_archive.append(self)
        print(len(list_of_archive))
        self.download_archive()


    def download_archive(self):
        with open(app.config['DATASAVE_PATH'] + self.file_name, "wb") as f:
            response = requests.get(self.link, stream=True)
            total_length = response.headers.get('content-length')

            if total_length is None:
                f.write(response.content)
            else:
                dl = 0
                total_length = int(total_length)
                for data in response.iter_content(chunk_size=4096):
                    dl += len(data)
                    self.progress = int(dl / (total_length / 100))
        # self.status = "ok"

    def get_status(self):
        log: dict
        if self.status == 'downloading':
            log = {"status": self.status, "progress": self.progress}
        # elif self.status == 'unpacking':
        #     log = {"status": self.status, "progress": self.progress}
        # else:
        #     log = {"status":self.status}

        return json.dumps(log)