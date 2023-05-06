import requests

from archives_app.Archive import Archive, list_of_archives, dict_of_archive_names
from archives_app import app


class Downloader(Archive):
    progress = 0
    status = "downloading"

    def __init__(self, link: str, id: int) -> None:

        self.id = id
        self.link = link
        self.file = self.link[self.link.rfind('/') + 1:]
        self.file_path = app.config['DATASAVE_PATH'] + self.file

        list_of_archives.append(self)
        dict_of_archive_names[self.file] = id

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

    def get_status(self) -> dict:

        log = {"status": self.status, "progress": self.progress}
        return log
