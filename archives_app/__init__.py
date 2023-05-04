import json

from flask import Flask, Response, request

from archives_app.DeleteFiles import DeleteFiles
from archives_app.Unpacking import Unpacking

app = Flask(__name__)
app.config.from_object('config')

from archives_app.Downloader import Downloader, list_of_archive


@app.route("/archive", methods=['POST'])
@app.route("/archive/<id>", methods=['GET', 'DELETE'])
def handler(id=None) -> Response | str:
    if request.method == 'POST':
        id = len(list_of_archive) + 1
        data = request.json
        response = app.response_class(response=json.dumps({'id': id}),
                                      status=200,
                                      mimetype='application/json')

        @response.call_on_close
        def on_close() -> None:
            archive = Downloader(link=data['url'], id=len(list_of_archive) + 1)
            list_of_archive[id - 1] = Unpacking(id, file_path=archive.file_path)

        return response

    try:
        if request.method == 'GET':
            return app.response_class(response=list_of_archive[int(id) - 1].get_status(),
                                      status=200,
                                      mimetype='application/json')

        if request.method == 'DELETE':
            archive = list_of_archive[int(id) - 1]
            DeleteFiles.deleteDir(archive.file_path)
            list_of_archive[int(id) - 1] = DeleteFiles(id, archive.file_path)
            return app.response_class(status=200)

    except IndexError:
        return app.response_class(
            response=json.dumps({'id': id, 'error': "Not found"}),
            status=404,
            mimetype='application/json'
        )
    except ValueError:
        return app.response_class(
            response=json.dumps({'error': "Invalid value"}),
            status=404,
            mimetype='application/json'
        )
