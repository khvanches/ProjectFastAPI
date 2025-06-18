from typing import Iterable, Type
from http import HTTPStatus
from fastapi import HTTPException

from sqlmodel import Session, select
from .engine import engine
from app.models.user import User


def get_user(user_id: int) -> User | None:
    with Session(engine) as session:
        return session.get(User, user_id)


def get_all_users() -> Iterable[User] | None:
    with Session(engine) as session:
        statement = select(User)
        return session.exec(statement).all()


def create_user(user: User) -> User:
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

def delete_user(user_id: int) -> User | None:
    with Session(engine) as session:
        db_user = session.get(User, user_id)
        if not db_user:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
        session.delete(db_user)
        session.commit()
        return db_user

def update_user(user_id: int, user: User) -> Type[User]:
    with Session(engine) as session:
        db_user = session.get(User, user_id)
        if not db_user:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
        user_data = user.model_dump(exclude_unset=True)
        db_user.sqlmodel_update(user_data)
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user
