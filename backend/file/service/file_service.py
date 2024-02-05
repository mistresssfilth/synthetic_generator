import os
import pandas as pd

from flask import current_app
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

app = current_app


class FileService:
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


