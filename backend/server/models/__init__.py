from sqlmodel import SQLModel, create_engine, Session
from .db_twitch import *
from .db_discord import *
from .db_sounds import *

# 初始化 SQLite 資料庫連線
DATABASE_URL = "sqlite:///./non_bot.db"
connect_args= {"check_same_thread": False}
engine = create_engine(DATABASE_URL, echo= False, connect_args= connect_args)

def get_session():
    with Session(engine) as session:
        yield session

def init_db():
    SQLModel.metadata.create_all(engine)