"""
이미지 업로드 및 조회 API 라우터 모듈.

이 모듈은 사용자 및 콘텐츠와 연결된 이미지를 업로드하고 조회하는 기능을 제공합니다.

작성자:
    kimdonghyeok
"""

import os
from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from starlette import status

from api.image import image_crud
from api.image.image_schema import ImageCreate
from api.user.user_router import get_current_user
from config.database_init import get_db

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "gif"}
router = APIRouter(
    prefix="/api",
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/token")


async def save_file(file: UploadFile, upload_dir: str = "/uploads/"):
    """
    파일을 지정된 디렉토리에 저장합니다.

    Args:
        file (UploadFile): 업로드된 파일 객체.
        upload_dir (str): 파일이 저장될 디렉토리 경로.

    Returns:
        str: 저장된 파일의 경로.

    Raises:
        HTTPException: 파일 저장 중 오류가 발생한 경우.
    """
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
    """
    사용자 이미지를 업로드하고 데이터베이스에 저장합니다.

    Args:
        current_user (dict): 현재 로그인된 사용자 정보.
        db (Session): SQLAlchemy 데이터베이스 세션.
        file (UploadFile): 업로드된 파일 객체.

    Returns:
        dict: 업로드 결과 및 저장된 이미지 ID.
    """
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
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
    files: List[UploadFile] = File(...),
):
    """
    콘텐츠와 연결된 이미지를 업로드하고 데이터베이스에 저장합니다.

    Args:
        current_user (dict): 현재 로그인된 사용자 정보.
        db (Session): SQLAlchemy 데이터베이스 세션.
        files (List[UploadFile]): 업로드된 파일 객체의 리스트.

    Returns:
        dict: 업로드 결과 및 저장된 이미지 ID 목록.
    """
    image_ids = []
    for file in files:
        try:
            saved_file_path = await save_file(file)
            _image_create = ImageCreate(image_address=saved_file_path)
            image_id = image_crud.create_contentimage(db=db, image_create=_image_create)
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
    """
    현재 사용자의 이미지를 조회합니다.

    Args:
        current_user (dict): 현재 로그인된 사용자 정보.
        db (Session): SQLAlchemy 데이터베이스 세션.

    Returns:
        dict: 사용자의 이미지 데이터.
    """
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
def get_contentimages(
    content_ids: List[int] = Query(...),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    콘텐츠와 연결된 이미지를 조회합니다.

    Args:
        content_ids (List[int]): 조회할 콘텐츠 ID 목록.
        current_user (dict): 현재 로그인된 사용자 정보.
        db (Session): SQLAlchemy 데이터베이스 세션.

    Returns:
        dict: 각 콘텐츠 ID에 연결된 이미지 데이터.
    """
    content_images_idx = {}
    for content_id in content_ids:
        content_images = image_crud.get_content_image(db, content_id)
        if not content_images:
            continue
        content_images_idx[content_id] = content_images
    if content_images_idx == {}:
        raise HTTPException(status_code=404, detail="Content images not found")
    return {
        "status_code": status.HTTP_200_OK,
        "detail": "이미지 정보가 업로드 되었습니다",
        "data": {"content_images ": content_images_idx},
    }
