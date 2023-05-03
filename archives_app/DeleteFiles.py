from archives_app.Archive import Archive


class DeleteFiles(Archive):

    def __init__(self,id:int,file:str):
        self.id = id
        self.file_name = file

    def delete(self):
        pass
