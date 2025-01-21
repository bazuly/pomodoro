from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_DRIVER: str
    DB_NAME: str
    CACHE_HOST: str
    CACHE_PORT: int
    CACHE_DB: int
    JWT_SECRET_KEY: str
    JWT_ENCODE_ALGORITHM: str
    GOOGLE_CLIENT_ID: str
    GOOGLE_SECRET_KEY: str
    GOOGLE_REDIRECT_URI: str
    GOOGLE_TOKEN_URL: str
    YANDEX_CLIENT_ID: str
    YANDEX_SECRET_KEY: str
    YANDEX_REDIRECT_URL: str
    YANDEX_TOKEN_URL: str

    class Config:
        env_file = ".env"

    @property
    def db_url(self):
        return f"{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def google_redirect_url(self) -> str:
        return (
            f"https://accounts.google.com/o/oauth2/auth?"
            f"response_type=code&client_id={self.GOOGLE_CLIENT_ID}&"
            f"redirect_uri={self.GOOGLE_REDIRECT_URI}&"
            f"scope=openid%20profile%20email&access_type=offline"
        )

    @property
    def yandex_redirect_url(self) -> str:
        return (
            f"https://oauth.yandex.ru/authorize?response_type=code&client_id={
            self.YANDEX_CLIENT_ID}&"
            f"redirect_uri={self.YANDEX_REDIRECT_URL}"
        )
