"""
이미지 및 인증 관련 스키마 정의 모듈.

이 모듈은 이미지 업로드, 인증 토큰, 콘텐츠-이미지 관계를 정의하는 Pydantic 모델을 제공합니다.

작성자:
    kimdonghyeok
"""

from pydantic import BaseModel


class ImageCreate(BaseModel):
    """
    이미지 생성 요청 데이터 모델.

    Attributes:
        image_address (str): 저장된 이미지의 주소.
    """
    image_address: str


class Token(BaseModel):
    """
    인증 토큰 데이터 모델.

    Attributes:
        access_token (str): 인증에 사용되는 액세스 토큰.
        token_type (str): 토큰의 유형 (예: Bearer).
        username (str): 토큰이 발급된 사용자의 이름.
    """
    access_token: str
    token_type: str
    username: str


class ContentImage(BaseModel):
    """
    콘텐츠-이미지 관계 데이터 모델.

    Attributes:
        content_id (int): 콘텐츠의 고유 ID.
    """
    content_id: int
