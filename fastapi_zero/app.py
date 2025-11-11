from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from fastapi_zero.database import get_session
from fastapi_zero.models import User
from fastapi_zero.schemas import (
    Message,
    UserList,
    UserPublic,
    UserSchema,
)

app = FastAPI(title='FastAPI Zero', version='0.1.0')


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá Mundo!'}


@app.get('/users/{user_id}', response_model=UserPublic)
def read_user__exercicio(user_id: int, session=Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    return db_user


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session=Depends(get_session)):
    db_user = session.scalar(
        select(User).where(
            User.username == user.username or User.email == user.email
        )
    )
    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Username já existe!',
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Email already exists!',
            )

    db_user = User(
        username=user.username,
        email=user.email,
        password=user.password,
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.get('/users/', response_model=UserList)
def read_users(skip: int = 0, limit: int = 100, session=Depends(get_session)):
    users = session.scalars(select(User).offset(skip).limit(limit)).all()
    return {'users': users}


@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(user_id: int, user: UserSchema, session=Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == user_id))
    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )
    try:
        db_user.username = user.username
        db_user.password = user.password
        db_user.email = user.email
        session.commit()
        session.refresh(db_user)
        return db_user
    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Username or Email already exists',
        )


@app.delete(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=Message
)
def delete_user(user_id: int, session=Depends(get_session)):
    user_db = session.scalar(select(User).where(User.id == user_id))
    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User not found',
        )
    session.delete(user_db)
    session.commit()
    return {'message': 'User deleted successfully'}
