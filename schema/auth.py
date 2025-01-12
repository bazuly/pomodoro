from pydantic import BaseModel


class GoogleUserData(BaseModel):
    sub: int
    email: str
    email_verified: bool
    name: str
    access_token: str
