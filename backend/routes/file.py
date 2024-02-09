from flask import Blueprint, jsonify, request, send_file, send_from_directory, current_app

from project.backend.db.entity.file import File
from project.backend.file.controller.file_controller import FileController
from project.backend.utils.token_required import token_required, get_user_by_token

FILE_REQUEST_API = Blueprint('request_file_api', __name__)

fileController = FileController()
app = current_app

def get_blueprint():
    """Return the blueprint for the main app module"""
    return FILE_REQUEST_API


@FILE_REQUEST_API.route('/upload', methods=['POST'])
@token_required
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
@token_required
def get_file_properties(filename):
    numerical, categorical = fileController.get_properties(filename)
    return jsonify(
        {
            "numerical": numerical,
            "categorical": categorical
        }
    ), 200


@FILE_REQUEST_API.route('/train', methods=['POST'])
@token_required
def train():
    user = get_user_by_token()

    data = request.get_json()
    try:
        filename = data['filename']
        numerical = data['numerical']
        categorical = data['categorical']
        batch_size = data['batchSize']
        learning_rate = data['learningRate']
        epochs = data['epochs']

        fileController.train(filename, batch_size, epochs, user.get_id())
        return jsonify({}), 200

    except KeyError:
        return jsonify({'error': 'Invalid request body'}), 400


@FILE_REQUEST_API.route('/generate', methods=['POST'])
@token_required
def generate():
    data = request.get_json()
    try:
        filename = data["filename"]
        epochs = data["rows"]

        file = fileController.generate(filename, epochs)

        return send_from_directory(app.config['UPLOAD_FOLDER'],
                                   file)

    except KeyError:
        return jsonify({'error': 'Invalid request body'}), 400


@FILE_REQUEST_API.route('/files', methods=['GET'])
@token_required
def get_files():
    user = get_user_by_token()

    items: list[File] = fileController.get_files(user.get_id())

    content = []
    for item in items:
        content.append(
            {
                "filename": item.get_filename,
                "id": str(item.get_id()),
            }
        )

    return jsonify(
        {
            "files": content
        }
    ), 200

