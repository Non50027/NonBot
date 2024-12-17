from sqlmodel import SQLModel, create_engine, Session

# 初始化 SQLite 資料庫連線
DATABASE_URL = "sqlite://N:/SQLiteData/non_bot.db"
engine = create_engine(DATABASE_URL, echo= True)

# 建立 SessionLocal
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_session():
    with Session(engine) as session:
        yield session

def init_db():
    SQLModel.metadata.create_all(engine)