from typing import Optional
from uuid import UUID, uuid4


class File:
    def __init__(
            self,
            filename: Optional[str],
            user_id: UUID,

            _id: Optional[UUID] = None,

    ):
        self.__id: UUID = _id or uuid4()
        self.__filename: str = filename
        self.__user_id: UUID = user_id

    def get_id(self) -> UUID:
        return self.__id

    def get_user_id(self) -> UUID:
        return self.__user_id

    def set_user_id(self, user_id: UUID):
        if isinstance(user_id, UUID):
            self.__user_id = user_id
        else:
            raise TypeError

    user_id = property(get_user_id, set_user_id)


    def get_filename(self) -> str:
        return self.__filename

    def set_filename(self, new_filename: str):
        if isinstance(new_filename, str):
            self.__filename = new_filename
        else:
            raise TypeError

    password = property(get_filename, set_filename)
