from flask import Flask, Response, request


app = Flask(__name__)
app.config.from_object('config')

from archives_app.Downloader import Downloader, list_of_archive

@app.route("/archive",methods=['POST'])
@app.route("/archive/<id>", methods = ['GET','DELETE'])
def handler(id=None):
    if request.method == 'POST':

        id = len(list_of_archive) + 1
        data = request.json
        response = Response(str(id))

        @response.call_on_close
        def on_close():

            archive = Downloader(link=data['url'], id=len(list_of_archive) + 1)
            print('here')
            print(len(list_of_archive))
            del archive
            print(len(list_of_archive))

        return response

    log: dict
    if request.method == 'GET':
        return list_of_archive[int(id)-1].get_status()

    if request.method == 'DELETE':
        pass



