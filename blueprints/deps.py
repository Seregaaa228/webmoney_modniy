
from crud import user_crud
from core.db import get_connection
from core import errors
from models.user import UserModel



def get_user_by_login(login: str) -> UserModel:
    with get_connection() as conn:
        user_data = user_crud.get(conn, login)

    if user_data is None:
        raise errors.NotFoundError(f"User with login '{login}' was not found")

    return user_data


def get_user_by_id(id: str) -> UserModel:
    with get_connection() as conn:
        user_data = user_crud.getbyId(conn, id)

    if user_data is None:
        raise errors.NotFoundError(f"User with id '{id}' was not found")

    return user_data
