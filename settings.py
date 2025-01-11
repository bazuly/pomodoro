from pydantic_settings import BaseSettings


# ofc the best practice is .env
class Settings(BaseSettings):
    DB_HOST: str = "0.0.0.0"
    DB_PORT: int = 5432
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "password"
    DB_DRIVER: str = "postgresql+psycopg2"
    DB_NAME: str = "pomodoro"
    CACHE_HOST: str = "0.0.0.0"
    CACHE_PORT: int = 6379
    CACHE_DB: int = 0
    JWT_SECRET_KEY: str = "secret"
    JWT_ENCODE_ALGORITHM: str = "HS256"
    GOOGLE_CLIENT_ID: str = "339375026924-ecpmk2o8a56fl04tm1tkmd2aikimgsb4.apps.googleusercontent.com"
    GOOGLE_SECRET_KEY: str = "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"
    GOOGLE_REDIRECT_URI: str = "http://localhost:8000/auth/google"
    GOOGLE_TOKEN_URL: str = "https://accounts.google.com/o/oauth2/token"

    @property
    def db_url(self):
        return f"{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def google_redirect_url(self) -> str:
        return f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={self.GOOGLE_CLIENT_ID}&redirect_uri={
            self.GOOGLE_REDIRECT_URI}&scope=openid%20profile%20email&access_type=offline"
