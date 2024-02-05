from werkzeug.datastructures import FileStorage

from backend.file.service.file_service import FileService

class FileController:
    def __init__(self):
        self.file_service = FileService()

    def upload(self, file: FileStorage) -> None:
        self.file_service.upload(file)

    def get_properties(self, filename: str) -> list[tuple: list, list]:
        return self.file_service.get_properties(filename)