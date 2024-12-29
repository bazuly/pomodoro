from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from settings import Settings

settings = Settings()
engine = create_engine("sqlite:///pomodoro.sqlite")
Session = sessionmaker(engine)

def get_db_connection():
    return Session
