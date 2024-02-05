from typing import List

from flask import current_app
from sqlalchemy import MetaData, Table, String, Integer, Column
from sqlalchemy.orm import Mapped

from backend.app_db import get_current_db

db = get_current_db(current_app)

class UserModel(db.Model):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}

    id = db.Column('user_id', Integer(), primary_key=True)

    email = db.Column(db.String(100))
    passwordHash = db.Column(db.String(70))


