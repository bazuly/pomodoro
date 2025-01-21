from pydantic import BaseModel, Field


class GoogleUserData(BaseModel):
    sub: int
    email: str
    email_verified: bool
    name: str
    access_token: str


class YandexUserData(BaseModel):
    id: int
    login: str
    name: str = Field(alias="real_name")
    default_email: str
    access_token: str
