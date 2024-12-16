"""
Pydantic 스키마 정의 모듈.

이 모듈은 콘텐츠 생성 요청 및 인증 토큰과 관련된 Pydantic 스키마를 정의합니다.

작성자:
    kimdonghyeok
"""

from typing import List

from fastapi import HTTPException
from pydantic import BaseModel, validator
from starlette import status


class ContentCreate(BaseModel):
    """
    콘텐츠 생성 요청 데이터 모델.

    Attributes:
        title (str): 콘텐츠 제목.
        content (str): 콘텐츠 내용.
        image_id (List): 첨부된 이미지 ID 목록.
    """

    title: str
    content: str
    image_id: List

    @validator("content", "title", pre=True, always=True)
    def not_empty(cls, v, field):
        """
        콘텐츠와 제목 필드가 비어 있지 않은지 확인하는 유효성 검사기.

        Args:
            v (str): 검증할 값.
            field (ModelField): 검증할 필드 정보.

        Returns:
            str: 유효한 값.

        Raises:
            HTTPException: 필드가 비어 있거나 공백인 경우 400 상태 코드와 오류 메시지를 반환.
        """
        if not v or not v.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{field.name}이(가) 비어있을 수 없습니다.",
            )
        return v


class Token(BaseModel):
    """
    인증 토큰 데이터 모델.

    Attributes:
        access_token (str): 인증에 사용되는 액세스 토큰.
        token_type (str): 토큰 유형 (예: Bearer).
    """
    access_token: str
    token_type: str
    # username: str
