"""
사용자 인증 및 관리 API 라우터 모듈.

이 모듈은 사용자 생성, 로그인, 토큰 발급, 사용자 정보 조회 등 인증 및 관리 기능을 제공합니다.

작성자:
    kimdonghyeok
"""

import os
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from starlette import status

from api.user import user_crud, user_schema
from api.user.user_crud import pwd_context
from config.database_init import get_db

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24
SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/token")

router = APIRouter(
    prefix="/api/user",
)


@router.post("/create", status_code=status.HTTP_200_OK)
def user_create(_user_create: user_schema.UserCreate, db: Session = Depends(get_db)):
    """
    새로운 사용자를 생성합니다.

    Args:
        _user_create (UserCreate): 생성할 사용자 데이터.
        db (Session): SQLAlchemy 데이터베이스 세션.

    Returns:
        dict: 생성 성공 메시지와 상태 코드.

    Raises:
        HTTPException: 사용자가 이미 존재할 경우 409 상태 코드 반환.
    """
    user = user_crud.get_existing_user(db, user_create=_user_create)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="이미 존재하는 사용자입니다."
        )
    user_crud.create_user(db=db, user_create=_user_create)

    return {
        "status_code": status.HTTP_200_OK,
        "detail": "정상적으로 생성되었습니다.",
    }


@router.post("/login")
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """
    사용자 로그인 및 액세스 토큰 발급.

    Args:
        form_data (OAuth2PasswordRequestForm): 사용자 로그인 데이터 (username, password).
        db (Session): SQLAlchemy 데이터베이스 세션.

    Returns:
        dict: 액세스 토큰 및 사용자 정보.

    Raises:
        HTTPException: 인증 실패 시 401 상태 코드 반환.
    """
    user = user_crud.get_user(db, form_data.username)
    if not user or not pwd_context.verify(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="아이디 혹은 패스워드가 일치하지 않습니다.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    data = {
        "sub": user.username,
        "exp": datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    }

    access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return {
        "status_code": status.HTTP_200_OK,
        "detail": "정상적으로 로그인되었습니다.",
        "data": {
            "access_token": access_token,
            "token_type": "bearer",
            "username": user.username,
        },
    }


@router.post("/token")
def login_for_access_token_with_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """
    사용자 로그인 및 액세스 토큰 발급 (중복 함수).

    Args:
        form_data (OAuth2PasswordRequestForm): 사용자 로그인 데이터 (username, password).
        db (Session): SQLAlchemy 데이터베이스 세션.

    Returns:
        dict: 액세스 토큰 정보.

    Raises:
        HTTPException: 인증 실패 시 401 상태 코드 반환.
    """
    user = user_crud.get_user(db, form_data.username)
    if not user or not pwd_context.verify(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="아이디 혹은 패스워드가 일치하지 않습니다.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    data = {
        "sub": user.username,
        "exp": datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    }

    access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": access_token, "token_type": "bearer"}


def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    현재 사용자의 정보를 토큰에서 추출합니다.

    Args:
        token (str): Bearer 토큰.

    Returns:
        dict: 현재 사용자의 정보 (username).

    Raises:
        HTTPException: 토큰 검증 실패 시 401 상태 코드 반환.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")

        if username is None:
            raise credentials_exception

        token_data = {"username": username}
    except JWTError:
        raise credentials_exception
    else:
        return token_data


@router.get("/me")
def read_users_me(current_user: dict = Depends(get_current_user)):
    """
    현재 로그인된 사용자의 정보를 반환합니다.

    Args:
        current_user (dict): 현재 로그인된 사용자 정보.

    Returns:
        dict: 현재 사용자의 정보.
    """
    return current_user
