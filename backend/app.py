from flask import Flask, make_response, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

import app_db
from backend.routes import file


def create_app(db_uri=app_db.SQLALCHEMY_DATABASE_URI):
    app = Flask(__name__)
    CORS(app, origins="http://localhost:3000", supports_credentials=True, methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['UPLOAD_FOLDER'] = 'D:/datasets'
    with app.app_context():
        db = SQLAlchemy(app)
        app.db = db

        from routes import auth
        from db.model import models

        app.register_blueprint(auth.get_blueprint())
        app.register_blueprint(file.get_blueprint())

        db.create_all()
        db.session.commit()


    @app.errorhandler(400)
    def handle_400_error(_error):
        return make_response(jsonify({'error': 'Misunderstood'}), 400)

    @app.errorhandler(401)
    def handle_401_error(_error):
        return make_response(jsonify({'error': 'Unauthorised'}), 401)

    @app.errorhandler(403)
    def handle_403_error(_error):
        return make_response(jsonify({'error': 'Forbidden'}), 403)

    @app.errorhandler(404)
    def handle_404_error(_error):
        return make_response(jsonify({'error': 'Not found'}), 404)

    @app.errorhandler(500)
    def handle_500_error(_error):
        return make_response(jsonify({'error': 'Server error'}), 500)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0')
