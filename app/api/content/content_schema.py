from typing import List

from fastapi import HTTPException
from pydantic import BaseModel, validator
from starlette import status


class ContentCreate(BaseModel):
    title: str
    content: str
    image_id: List

    @validator("content", "title", pre=True, always=True)
    def not_empty(cls, v, field):
        if not v or not v.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{field.name}이(가) 비어있을 수 없습니다.",
            )
        return v


class Token(BaseModel):
    access_token: str
    token_type: str
    # username: str
