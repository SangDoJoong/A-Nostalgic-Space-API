"""
사용자 관련 데이터 처리 모듈.

이 모듈은 사용자 생성, 조회 및 인증 관련 데이터베이스 작업을 처리합니다.

작성자:
    kimdonghyeok
"""

import pendulum
from fastapi import HTTPException
from passlib.context import CryptContext
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from api.user.user_schema import UserCreate
from models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user(db: Session, user_create: UserCreate):
    """
    새로운 사용자를 생성하고 데이터베이스에 저장합니다.

    Args:
        db (Session): SQLAlchemy 데이터베이스 세션.
        user_create (UserCreate): 생성할 사용자 데이터.

    Returns:
        User: 생성된 사용자 객체.

    Raises:
        HTTPException: 데이터베이스 작업 중 오류가 발생한 경우.
    """
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
    """
    이미 존재하는 사용자를 조회합니다.

    Args:
        db (Session): SQLAlchemy 데이터베이스 세션.
        user_create (UserCreate): 조회할 사용자 데이터.

    Returns:
        User or None: 사용자 객체 또는 존재하지 않을 경우 None.
    """
    return db.query(User).filter(User.username == user_create.username).first()


def get_user(db: Session, username: str):
    """
    사용자 이름으로 사용자를 조회합니다.

    Args:
        db (Session): SQLAlchemy 데이터베이스 세션.
        username (str): 조회할 사용자의 이름.

    Returns:
        User or None: 사용자 객체 또는 존재하지 않을 경우 None.
    """
    return db.query(User).filter(User.username == username).first()
