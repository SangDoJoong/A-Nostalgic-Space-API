"""
콘텐츠 생성 및 조회 관련 함수 모듈.

이 모듈은 데이터베이스에서 콘텐츠를 생성하거나 특정 사용자와 관련된 콘텐츠를 조회하는 기능을 제공합니다.

작성자:
    kimdonghyeok
"""


import pendulum
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from api.content.content_schema import ContentCreate
from models import Content


def create_content(current_user: dict, db: Session, content_create: ContentCreate):

    """
    새로운 콘텐츠를 데이터베이스에 생성합니다.

    Args:
        current_user (dict): 현재 로그인된 사용자 정보.
        db (Session): SQLAlchemy 데이터베이스 세션.
        content_create (ContentCreate): 생성할 콘텐츠의 데이터.

    Returns:
        int: 생성된 콘텐츠의 고유 ID.

    Raises:
        HTTPException: 데이터베이스 작업 중 오류가 발생한 경우 500 상태 코드 반환.
    """

    try:

        db_content = Content(
            content=content_create.content,
            created_at=pendulum.now("Asia/Seoul"),
            title=content_create.title,
            writer_name=current_user["username"],
            like_cnt=0,
            is_deleted=False,
        )
        db.add(db_content)
        db.flush()

        db.commit()

        return db_content.contents_id

    except SQLAlchemyError as e:
        db.rollback()  # 데이터베이스 롤백
        print(f"An error occurred: {e}")  # 오류 메시지 출력 또는 로깅
        raise HTTPException(status_code=500, detail="Internal Server Error")


def get_user_content(db: Session, username: str):

    """
    특정 사용자가 작성한 콘텐츠 ID 목록을 조회합니다.

    Args:
        db (Session): SQLAlchemy 데이터베이스 세션.
        username (str): 조회할 사용자의 이름.

    Returns:
        list: 사용자가 작성한 콘텐츠 ID의 목록.

    Raises:
        HTTPException: 데이터베이스 작업 중 오류가 발생한 경우 500 상태 코드 반환.
    """

    try:

        contents_list = [
            content.contents_id
            for content in db.query(Content)
            .filter(Content.writer_name == username)
            .all()
        ]

        return contents_list
    except SQLAlchemyError as e:
        db.rollback()  # 데이터베이스 롤백
        print(f"An error occurred: {e}")  # 오류 메시지 출력 또는 로깅
        raise HTTPException(status_code=500, detail="Internal Server Error")
