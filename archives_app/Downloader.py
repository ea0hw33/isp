import json
import requests
from archives_app.Archive import Archive
from archives_app import app

list_of_archive = []


class Downloader(Archive):
    progress = 0
    status = "downloading"

    def __init__(self, link: str, id: int) -> None:

        list_of_archive.append(self)

        self.id = id
        self.link = link
        self.file = self.link[self.link.rfind('/') + 1:]
        self.file_path = app.config['DATASAVE_PATH'] + self.file
        self.download_archive()

    def download_archive(self) -> None:
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
                    self.track_progress(total_length, dl)

        self.status = 'unpacking'
        self.progress = 0

    def track_progress(self, total: int, dl: int) -> None:
        self.progress = int(dl / (total / 100))

    def get_status(self) -> str:

        log = {"status": self.status, "progress": self.progress}
        return json.dumps(log)
