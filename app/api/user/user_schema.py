from fastapi import HTTPException
from pydantic import BaseModel, validator
from starlette import status


class UserCreate(BaseModel):
    username: str
    password1: str
    password2: str

    @validator("username", "password1", "password2")
    def not_empty(cls, v):
        if not v or not v.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="빈 값은 허용되지 않습니다.",
            )
        return v

    @validator("password2")
    def passwords_match(cls, v, values):
        if "password1" in values and v != values["password1"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="비밀번호가 일치하지 않습니다",
            )
        return v


class Token(BaseModel):
    access_token: str
    token_type: str
    username: str
