from uuid import UUID

from flask import current_app

from backend.app_db import get_current_db
from backend.db.entity.user import User
from backend.exceptions.exceptions import UserNotFoundException

db = get_current_db(current_app)

class UserRepository:

    def get_user_by_id(self, _id: UUID):
        from backend.db.model.models import UserModel
        user: UserModel = UserModel.query.filter_by(id=str(_id)).first()
        if user is None:
            raise UserNotFoundException
        return User(
            _id=UUID(hex=user.id),
            email=user.email,
            password=user.passwordHash,
        )

    def get_user_by_email(self, email: str) -> User:
        from backend.db.model.models import UserModel
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
        from backend.db.model.models import UserModel
        user: UserModel = UserModel(
            id=str(new_user.get_id()),
            email=new_user.email,
            passwordHash=new_user.password,
        )

        db.session.add(user)
        db.session.commit()
