"""
데이터베이스 모델 정의 모듈.

이 모듈은 데이터베이스에 저장될 사용자, 이미지, 사용자-이미지 관계, 콘텐츠-이미지 관계와 관련된 모델을 정의합니다.

작성자:
    kimdonghyeok
"""

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from config.database_init import Base

class User(Base):
    """
    사용자 모델.

    데이터베이스에 저장될 사용자 정보를 나타냅니다.

    Attributes:
        uid (int): 사용자 고유 식별자.
        password (str): 사용자 비밀번호.
        created_at (datetime): 사용자 계정 생성일.
        username (str): 사용자 이름.
    """
    __tablename__ = "Users"

    uid = Column(Integer, primary_key=True)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    username = Column(String, nullable=False)


class Content(Base):
    """
    콘텐츠 모델.

    데이터베이스에 저장될 콘텐츠 정보를 나타냅니다.

    Attributes:
        contents_id (int): 콘텐츠 고유 식별자.
        title (str): 콘텐츠 제목.
        content (str): 콘텐츠 내용.
        writer_name (str): 작성자 이름.
        created_at (datetime): 콘텐츠 생성일.
        like_cnt (int): 콘텐츠 좋아요 수.
        is_deleted (bool): 콘텐츠 삭제 여부.
    """
    __tablename__ = "Contents"

    contents_id = Column(Integer, primary_key=True)
    title = Column(String, nullable=True)
    content = Column(String, nullable=True)
    writer_name = Column(String, primary_key=False)
    created_at = Column(DateTime, nullable=False)
    like_cnt = Column(Integer, nullable=False)
    is_deleted = Column(Boolean, nullable=False)


class Image(Base):
    """
    이미지 모델.

    데이터베이스에 저장될 이미지 정보를 나타냅니다.

    Attributes:
        image_id (int): 이미지 고유 식별자.
        image_address (str): 이미지 파일 경로 또는 URL.
        created_at (datetime): 이미지 생성일.
    """
    __tablename__ = "Images"

    image_id = Column(Integer, primary_key=True)
    image_address = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)


class UserImage(Base):
    """
    사용자-이미지 관계 모델.

    사용자가 업로드한 이미지와의 관계를 나타냅니다.

    Attributes:
        id (int): 고유 식별자.
        user_id (int): 사용자 ID.
        image_id (int): 이미지 ID.
    """
    __tablename__ = "Users_Images"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, primary_key=False)
    image_id = Column(Integer, primary_key=False)


class ContentImage(Base):
    """
    콘텐츠-이미지 관계 모델.

    콘텐츠와 첨부된 이미지 간의 관계를 나타냅니다.

    Attributes:
        id (int): 고유 식별자.
        content_id (int): 콘텐츠 ID.
        image_id (int): 이미지 ID.
    """
    __tablename__ = "Contents_Images"
    id = Column(Integer, primary_key=True)
    content_id = Column(Integer, primary_key=False)
    image_id = Column(Integer, primary_key=False)
