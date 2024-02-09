from flask import current_app
from sqlalchemy import Integer

from project.backend.app_db import get_current_db

db = get_current_db(current_app)

class UserModel(db.Model):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}

    id = db.Column('user_id', db.String, primary_key=True)

    email = db.Column(db.String(100))
    passwordHash = db.Column(db.String(70))


class FileModel(db.Model):
    __tablename__ = "file"
    __table_args__ = {'extend_existing': True}

    id = db.Column('request_id', db.String, primary_key=True)

    filename = db.Column(db.String, nullable=False)

    user_id = db.Column(db.String, db.ForeignKey("user.user_id"))


