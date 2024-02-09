from project.backend.auth.service.auth_service import AuthService
from project.backend.db.entity.user import User


class AuthController:

    def __init__(self):
        self.auth_service = AuthService()

    def register(self, email: str, password: str) -> None:
        self.auth_service.register(email, password)

    def login(self, email: str, password: str) -> str:
        return self.auth_service.login(email, password)

    def authentication(self, token: str) -> User:
        return self.auth_service.authentication(token)
