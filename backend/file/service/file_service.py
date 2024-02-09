import os
import pandas as pd

from flask import current_app
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from project.backend.db.entity.file import File
from project.backend.db.model.models import UserModel, FileModel
from project.backend.db.repository.user_repository import UserRepository
from project.backend.gan import Gan

app = current_app


class FileService:
    def __init__(self):
        self.user_repository = UserRepository()

    def upload(self, file: FileStorage):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    def get_properties(self, filename: str):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        df = pd.read_csv(file_path)

        # Получить список столбцов с числовыми значениями
        numerical_columns = df.select_dtypes(include=['number']).columns.tolist()
        # Определение порогового значения уникальных значений для категориальных столбцов
        threshold_unique_values = 10  # Порог можно выбрать на своё усмотрение

        # Получение списка столбцов с категориальными характеристиками на основании уникальных значений
        categorical_columns = []
        for column in df.columns:
            unique_values_count = df[column].nunique()
            if unique_values_count <= threshold_unique_values:
                categorical_columns.append(column)

        return numerical_columns, categorical_columns

    def train(self, filename: str, batch_size: float, epochs: int, user_id: int):
        gan_model = self.get_gan(filename)
        gan_model.train(epochs, batch_size, 10)
        self.user_repository.add_file(user_id, filename)

    @staticmethod
    def get_gan(filename: str):
        cc_scaled_data, col_max, cc_data = FileService.process_csv(filename)
        return Gan(cc_scaled_data, col_max)

    @staticmethod
    def process_csv(filename: str):
        # Input: The path location of the CSV
        # Outputs:
        #       1. The CSV scaled down to be between -1 and 1
        #       2. An array of maximum absolute values for each column.

        real_full_data = pd.read_csv(filename, header=0)
        real_full_data = real_full_data.apply(pd.to_numeric, errors='coerce')

        # Удаляем строки, содержащие пропущенные значения (NaN)
        real_full_data = real_full_data.dropna()

        # Store the maximum absolute value of each column.
        col_max_array = real_full_data.abs().max().to_frame()

        # Scale the data to be between -1, 1
        real_scaled_data = real_full_data / real_full_data.abs().max()

        return real_scaled_data, col_max_array, real_full_data

    def generate_data(self, filename: str, epochs: int):
        gan_model = self.get_gan(filename)
        list_of_fakes = gan_model.gen_fake_data(epochs)
        file_path = 'D:\\datasets'
        fullname = os.path.join(file_path, 'fake_' + filename)
        list_of_fakes.to_csv(fullname, index=False)

        return 'fake_' + filename

    @staticmethod
    def get_files(user_id) -> list[File]:

        user: UserModel = UserModel.query.filter_by(user_id=user_id).first()
        files: list[FileModel] = FileModel.query.filter(
            FileModel.user_id == user.id
        ).all()

        return files

