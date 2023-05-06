from flask import Flask, Response, request, jsonify

from archives_app.Archive import dict_of_archive_names, list_of_archives
from archives_app.DeleteFiles import DeleteFiles
from archives_app.Unpacking import Unpacking
from archives_app.User import User

app = Flask(__name__)
app.config.from_object('config')

from archives_app.Downloader import Downloader


@app.route("/archive", methods=['POST'])
@app.route("/archive/<id>", methods=['GET', 'DELETE'])
def handler(id=None) -> tuple[Response, int] | Response:

    if id is None:
        file_name = request.json['url']
        file_name = file_name[file_name.rfind('/')+1:]
        if file_name in dict_of_archive_names:
            return jsonify(id=dict_of_archive_names[file_name]), 200

    if request.method == 'POST':
        id = len(list_of_archives) + 1
        data = request.json

        response = jsonify(id=id)

        @response.call_on_close
        def on_close() -> None:
            archive = Downloader(link=data['url'], id=len(list_of_archives) + 1)
            list_of_archives[id - 1] = Unpacking(id, file_path=archive.file_path)

        return response, 200

    try:
        if request.method == 'GET':
            return jsonify(list_of_archives[int(id) - 1].get_status()), 200

        if request.method == 'DELETE':
            status = list_of_archives[int(id) - 1].get_status()['status']
            if status == 'downloading':
                raise PermissionError
            elif status == 'deleted':
                raise FileNotFoundError

            list_of_archives[int(id) - 1] = \
                DeleteFiles(int(id), list_of_archives[int(id) - 1].file_path)
            return app.response_class(status=200)

    except IndexError:
        return jsonify(id=id, error="Not found"), 404

    except ValueError:
        return jsonify(error="Invalid value"), 404

    except FileNotFoundError:
        return jsonify(error='File not found'), 404

    except PermissionError:
        return jsonify(error='File writing or reading now in another place'), 404