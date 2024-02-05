from flask import Blueprint, jsonify, request, current_app
from backend.file.controller.file_controller import FileController

FILE_REQUEST_API = Blueprint('request_file_api', __name__)

fileController = FileController()

def get_blueprint():
    """Return the blueprint for the main app module"""
    return FILE_REQUEST_API

@FILE_REQUEST_API.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    if file:
        fileController.upload(file)
        return 'File uploaded successfully', 200
    return 'An error occurred while attempting to upload the file', 500

@FILE_REQUEST_API.route('/properties/<filename>', methods=['GET'])
def get_file_properties(filename):
    numerical, categorical = fileController.get_properties(filename)
    return jsonify(
        {
            "numerical": numerical,
            "categorical": categorical
        }
    ), 200