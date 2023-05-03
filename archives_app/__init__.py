import json

from flask import Flask, request

from archives_app.Downloader import Downloader, list_of_archive

app = Flask(__name__)

@app.route("/archive",methods=['POST'])
@app.route("/archive/<id>", methods = ['GET','DELETE'])
def handler():
    if request.method == 'POST':
        data = json.loads(request.data)
        download = Downloader(link = data['url'],id = len(list_of_archive)+1 )

        return str(download.id)
    log: dict
    if request.method == 'GET':
        return

