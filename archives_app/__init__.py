from flask import Flask, Response, request

from archives_app.DeleteFiles import DeleteFiles
from archives_app.Unpacking import Unpacking

app = Flask(__name__)
app.config.from_object('config')

from archives_app.Downloader import Downloader, list_of_archive

@app.route("/archive",methods=['POST'])
@app.route("/archive/<id>", methods = ['GET','DELETE'])
def handler(id=None):
    if request.method == 'POST':

        id = len(list_of_archive) + 1
        print(id)
        data = request.json
        response = Response(str(id))

        @response.call_on_close
        def on_close():

            print(id)
            archive = Downloader(link=data['url'], id=len(list_of_archive) + 1)
            print(id)
            list_of_archive[id-1] = Unpacking(id, file_path=archive.file_path)
            print(id)

        return response

    log: dict
    if request.method == 'GET':
        return list_of_archive[int(id)-1].get_status()

    if request.method == 'DELETE':
        archive = list_of_archive[int(id)-1]
        DeleteFiles.deleteDir(archive.file_path)
        return 'ok'



