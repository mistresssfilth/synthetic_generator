from uuid import UUID

from flask import current_app

from project.backend.app_db import get_current_db
from project.backend.db.entity.user import User
from project.backend.exceptions.exceptions import UserNotFoundException
from project.backend.db.model.models import UserModel, FileModel

db = get_current_db(current_app)


class UserRepository:

    def get_user_by_id(self, _id: UUID):
        user: UserModel = UserModel.query.filter_by(id=str(_id)).first()
        if user is None:
            raise UserNotFoundException
        return User(
            _id=UUID(hex=user.id),
            email=user.email,
            password=user.passwordHash,
        )

    def get_user_by_email(self, email: str) -> User:
        user: UserModel = UserModel.query.filter_by(email=email).first()
        if user is None:
            raise UserNotFoundException
        return User(
            _id=UUID(hex=user.id),
            email=user.email,
            password=user.passwordHash,
        )

    @staticmethod
    def create_user(new_user: User) -> None:
        user: UserModel = UserModel(
            id=str(new_user.get_id()),
            email=new_user.email,
            passwordHash=new_user.password,
        )

        db.session.add(user)
        db.session.commit()

    @staticmethod
    def add_file(user_id, filename: str) -> None:
        file: FileModel = FileModel(
            filename=filename,
            user_id=user_id,
        )
        db.session.add(file)
        db.session.commit()
