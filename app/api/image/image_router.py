import os
from datetime import datetime
from typing import List

from api.image import image_crud
from api.image.image_schema import ImageCreate
from api.user.user_router import get_current_user
from config.database_init import get_db
from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, UploadFile
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from starlette import status

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "gif"}
router = APIRouter(
    prefix="/api",
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/token")


async def save_file(file: UploadFile, upload_dir: str = "/uploads/") -> str:
    try:
        file_contents = await file.read()
        _, file_extension = os.path.splitext(file.filename)
        file_name = f"{datetime.now().strftime('%Y%m%d%H%M%S%f')}{file_extension}"
        saved_file_path = os.path.join(upload_dir, file_name)  # 이미지를 저장할 경로
        with open(saved_file_path, "wb") as f:
            f.write(file_contents)
        return saved_file_path
    except Exception as e:
        print(f"Error reading file {file.filename}: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to save file {file.filename}"
        )


@router.post("/userimage")
async def upload_userimage(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
    file: UploadFile = File(...),
):

    image_ids = []
    try:
        saved_file_path = await save_file(file)
        _image_create = ImageCreate(image_address=saved_file_path)
        image_id = image_crud.create_userimage(
            db=db, image_create=_image_create, username=current_user.username
        )
        image_ids.append(image_id)
    except HTTPException as e:
        raise e

    return {
        "status_code": status.HTTP_200_OK,
        "detail": "정상적으로 저장되었습니다.",
        "data": {"image_id_index ": image_ids},
    }


@router.post("/contentimage")
async def upload_contentimage(
    db: Session = Depends(get_db),
    files: List[UploadFile] = File(...),
    content_id: int = Form(...),
):

    image_ids = []
    for file in files:
        try:
            saved_file_path = await save_file(file)
            _image_create = ImageCreate(image_address=saved_file_path)
            image_id = image_crud.create_contentimage(
                db=db, image_create=_image_create, content_id=content_id
            )
            image_ids.append(image_id)
        except HTTPException as e:
            raise e

    return {
        "status_code": status.HTTP_200_OK,
        "detail": "정상적으로 저장되었습니다.",
        "data": {"image_id_index ": image_ids},
    }


@router.get("/userimage")
def get_userimages(
    current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)
):
    _username = current_user["username"]

    user_images = image_crud.get_user_image(db, _username)
    if not user_images:
        raise HTTPException(status_code=404, detail="User images not found")
    return {
        "status_code": status.HTTP_200_OK,
        "detail": "이미지 정보가 업로드 되었습니다",
        "data": {"image_id_index ": user_images},
    }


@router.get("/contentimage")
def get_contentimages(content_id: str = Query(...), db: Session = Depends(get_db)):

    user_images = image_crud.get_content_image(db, content_id)
    if not user_images:
        raise HTTPException(status_code=404, detail="User images not found")
    return {
        "status_code": status.HTTP_200_OK,
        "detail": "이미지 정보가 업로드 되었습니다",
        "data": {"image_id_index ": user_images},
    }
