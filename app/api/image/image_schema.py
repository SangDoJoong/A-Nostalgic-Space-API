from pydantic import BaseModel


class ImageCreate(BaseModel):

    image_address: str


class Token(BaseModel):
    access_token: str
    token_type: str
    username: str
