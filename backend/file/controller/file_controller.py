from pandas import DataFrame
from werkzeug.datastructures import FileStorage

from project.backend.db.entity.file import File
from project.backend.file.service.file_service import FileService


class FileController:
    def __init__(self):
        self.file_service = FileService()

    def upload(self, file: FileStorage) -> None:
        self.file_service.upload(file)

    def get_properties(self, filename: str) -> list[tuple: list, list]:
        return self.file_service.get_properties(filename)

    def train(self, filename: str, batch_size: float, epochs: int, user_id: int) -> None:
        self.file_service.train(filename, batch_size, epochs)

    def generate(self, filename: str, epochs: int) -> str:
        return self.file_service.generate_data(filename, epochs)

    def get_files(self, user_id: int) -> list[File]:
        return self.file_service.get_files(user_id)
