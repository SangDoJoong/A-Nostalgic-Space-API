import pendulum
from fastapi import HTTPException
from passlib.context import CryptContext
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from api.user.user_schema import UserCreate
from models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user(db: Session, user_create: UserCreate):
    try:

        db_user = User(
            username=user_create.username,
            password=pwd_context.hash(user_create.password1),
            created_at=pendulum.now("Asia/Seoul"),
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)  # db_user 객체를 갱신하여 반환
        return db_user
    except SQLAlchemyError as e:
        db.rollback()  # 오류 발생 시 롤백
        error_msg = f"An error occurred while creating the user: {str(e)}"
        print(error_msg)  # 오류 메시지를 콘솔에 출력
        raise HTTPException(status_code=500, detail=error_msg)


def get_existing_user(db: Session, user_create: UserCreate):
    return db.query(User).filter(User.username == user_create.username).first()


def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()
