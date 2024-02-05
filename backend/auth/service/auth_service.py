from base64 import encode, decode
from uuid import UUID

from bcrypt import checkpw, gensalt, hashpw
from oauthlib.oauth2.rfc6749.errors import InvalidTokenError

from backend.db.entity.user import User
from backend.db.repository.user_repository import UserRepository
from backend.exceptions.exceptions import AlreadyExistException, UserNotFoundException, InvalidCredentialsException


class AuthService:
    def __init__(self):
        self.user_repository = UserRepository()

    def register(self, email: str, password: str) -> None:
        try:
            self.user_repository.get_user_by_email(email)
            raise AlreadyExistException
        except UserNotFoundException:
            new_user = User(
                email = email,
                password = password
            )
            hash = hashpw(str(new_user.password).encode(), gensalt())
            new_user.password = hash.decode()
            self.user_repository.create_user(new_user)

    def login(self, email: str, password: str) -> str:
        try:
            user = self.user_repository.get_user_by_email(email)
            if checkpw(password.encode(), str(user.password).encode()) is False:
                raise InvalidCredentialsException
            token = encode({"id": str(user.get_id())}, "SUPER-SECRET-KEY", algorithm="HS256")
            return token
        except UserNotFoundException:
            raise InvalidCredentialsException

    def authentication(self, token: str) -> User:
        try:
            payload = decode(token, "SUPER-SECRET-KEY", ["HS256"])
            _id = UUID(hex=payload["id"])
            return self.user_repository.get_user_by_id(_id)
        except Exception:
            raise InvalidTokenError


