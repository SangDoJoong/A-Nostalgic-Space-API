"""
이미지 및 관계 데이터 관리 모듈.

이 모듈은 이미지 데이터를 생성하거나 조회하고, 사용자-이미지 및 콘텐츠-이미지 관계를 처리하는 기능을 제공합니다.

작성자:
    kimdonghyeok
"""

import pendulum
from dotenv import load_dotenv
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from api.image.image_schema import ImageCreate
from models import ContentImage, Image, User, UserImage

load_dotenv()


def create_contentimage(db: Session, image_create: ImageCreate):
    """
    콘텐츠와 연결된 이미지를 생성합니다.

    Args:
        db (Session): SQLAlchemy 데이터베이스 세션.
        image_create (ImageCreate): 생성할 이미지의 데이터.

    Returns:
        int: 생성된 이미지의 고유 ID.

    Raises:
        HTTPException: 데이터베이스 작업 중 오류가 발생한 경우.
    """
    try:
        db_image = Image(
            created_at=pendulum.now("Asia/Seoul"),
            image_address=image_create.image_address,
        )
        db.add(db_image)
        db.commit()
        return db_image.image_id
    except SQLAlchemyError as e:
        db.rollback()  # 데이터베이스 롤백
        print(f"An error occurred: {e}")  # 오류 메시지 출력 또는 로깅
        raise HTTPException(status_code=500, detail="Internal Server Error")


def create_userimage(db: Session, image_create: ImageCreate, username: str):
    """
    사용자의 이미지를 생성하거나 업데이트합니다.

    Args:
        db (Session): SQLAlchemy 데이터베이스 세션.
        image_create (ImageCreate): 생성할 이미지의 데이터.
        username (str): 이미지를 연결할 사용자 이름.

    Returns:
        int: 생성 또는 업데이트된 이미지의 고유 ID.

    Raises:
        HTTPException: 데이터베이스 작업 중 오류가 발생한 경우.
    """
    try:
        user_id = db.query(User).filter(User.username == username).first().uid
        # 사용자가 기존에 이미지를 가지고 있는지 확인
        existing_user_image = (
            db.query(UserImage).filter(UserImage.user_id == user_id).first()
        )
        # image db 에 이미지 저장 정보 저장
        db_image = Image(
            created_at=pendulum.now("Asia/Seoul"),
            image_address=image_create.image_address,
        )
        db.add(db_image)
        db.flush()
        if existing_user_image:
            # 사용자가 기존 이미지를 가지고 있다면 해당 이미지 정보를 업데이트
            existing_user_image.image_id = db_image.image_id
            db.add(existing_user_image)
        else:
            # 사용자가 기존 이미지를 가지고 있지 않다면 새로운 UserImage 관계를 추가
            user_image = UserImage(user_id=user_id, image_id=db_image.image_id)
            db.add(user_image)
        db.commit()
        return db_image.image_id
    except SQLAlchemyError as e:
        db.rollback() # 데이터베이스 롤백
        print(f"An error occurred: {e}") # 오류 메시지 출력 또는 로깅
        raise HTTPException(status_code=500, detail="Internal Server Error")


def get_user_image(db: Session, username: str):
    """
    특정 사용자의 이미지 주소를 조회합니다.

    Args:
        db (Session): SQLAlchemy 데이터베이스 세션.
        username (str): 조회할 사용자 이름.

    Returns:
        str: 사용자의 이미지 주소.

    Raises:
        HTTPException: 데이터베이스 작업 중 오류가 발생한 경우.
    """
    try:
        user_image_id = db.query(User).filter(User.username == username).first().uid
        image_id = (
            db.query(UserImage)
            .filter(UserImage.user_id == user_image_id)
            .first()
            .image_id
        )
        image_address = (
            db.query(Image).filter(Image.image_id == image_id).first().image_address
        )
        return image_address
    except SQLAlchemyError as e:
        db.rollback()  # 데이터베이스 롤백
        print(f"An error occurred: {e}") # 오류 메시지 출력 또는 로깅
        raise HTTPException(status_code=500, detail="Internal Server Error")


def get_content_image(db: Session, content_id: str):
    """
    특정 콘텐츠와 연결된 모든 이미지 주소를 조회합니다.

    Args:
        db (Session): SQLAlchemy 데이터베이스 세션.
        content_id (str): 조회할 콘텐츠의 고유 ID.

    Returns:
        list: 콘텐츠와 연결된 이미지 주소 목록.

    Raises:
        HTTPException: 데이터베이스 작업 중 오류가 발생한 경우.
    """
    try:
        image_address = []
        results = (
            db.query(ContentImage).filter(ContentImage.content_id == content_id).all()
        )
        for result in results:
            image_id = result.image_id
            image_address.append(
                db.query(Image).filter(Image.image_id == image_id).first().image_address
            )
        return image_address
    except SQLAlchemyError as e:
        db.rollback()  # 데이터베이스 롤백
        print(f"An error occurred: {e}")  # 오류 메시지 출력 또는 로깅
        raise HTTPException(status_code=500, detail="Internal Server Error")
