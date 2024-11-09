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

    try:

        contents_id = content_crud.create_content(
            current_user, db=db, content_create=content_create
        )

        return {
            "status_code": status.HTTP_200_OK,
            "detail": "정상적으로 저장되었습니다.",
            "data": {"contents_id ": contents_id},
        }
    except HTTPException as e:
        raise e


@router.get("/mycontent")
def content_refresh(
    current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)
):

    try:

        content_list = content_crud.get_user_content(db, current_user["username"])
        print(content_list)
        return {
            "status_code": status.HTTP_200_OK,
            "detail": "정상적으로 저장되었습니다.",
            "data": {"content_ids ": content_list},
        }
    except HTTPException as e:
        raise e
