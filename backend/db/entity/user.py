from typing import Optional
from uuid import UUID, uuid4


class User:
    def __init__(self,
                 email: Optional[str],
                 password: Optional[str],
                 _id: Optional[UUID] = None
                 ):
        self.__id: UUID = _id or uuid4()
        self.__email: str = email
        self.__password: str = password

    def get_id(self) -> UUID:
        return self.__id

    def get_email(self) -> str:
        return self.__email

    def set_email(self, new_email: str):
        if isinstance(new_email, str):
            self.__email = new_email
        else:
            raise TypeError

    email = property(get_email, set_email)

    def get_password(self) -> str:
        return self.__password

    def set_password(self, new_password: str):
        if isinstance(new_password, str):
            self.__password = new_password
        else:
            raise TypeError

    password = property(get_password, set_password)