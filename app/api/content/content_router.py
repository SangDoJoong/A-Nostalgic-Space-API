"""
콘텐츠 API 라우터 모듈.

이 모듈은 콘텐츠 생성 및 조회와 관련된 엔드포인트를 제공합니다.

작성자:
    kimdonghyeok
"""

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from starlette import status

from api.content import content_crud
from api.content.content_schema import ContentCreate
from api.user.user_router import get_current_user
from config.database_init import get_db

router = APIRouter(
    prefix="/api/content",
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/token")


@router.post("/create")
async def content_create(
    content_create: ContentCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    새로운 콘텐츠를 생성합니다.

    Args:
        content_create (ContentCreate): 생성할 콘텐츠의 데이터.
        db (Session): SQLAlchemy 데이터베이스 세션.
        current_user (dict): 현재 로그인된 사용자 정보.

    Returns:
        dict: 생성된 콘텐츠 ID와 상태 정보를 포함하는 응답.

    Raises:
        HTTPException: 콘텐츠 생성 중 오류가 발생한 경우.
    """
    try:
        contents_id = content_crud.create_content(
            current_user, db=db, content_create=content_create
        )

        return {
            "status_code": status.HTTP_200_OK,
            "detail": "정상적으로 저장되었습니다.",
            "data": {"contents_id": contents_id},
        }
    except HTTPException as e:
        raise e


@router.get("/mycontent")
def content_refresh(
    current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)
):
    """
    현재 사용자가 생성한 콘텐츠 ID 목록을 조회합니다.

    Args:
        current_user (dict): 현재 로그인된 사용자 정보.
        db (Session): SQLAlchemy 데이터베이스 세션.

    Returns:
        dict: 사용자가 생성한 콘텐츠 ID 목록과 상태 정보를 포함하는 응답.

    Raises:
        HTTPException: 콘텐츠 조회 중 오류가 발생한 경우.
    """
    try:
        content_list = content_crud.get_user_content(db, current_user["username"])
        print(content_list)
        return {
            "status_code": status.HTTP_200_OK,
            "detail": "정상적으로 저장되었습니다.",
            "data": {"content_ids": content_list},
        }
    except HTTPException as e:
        raise e
