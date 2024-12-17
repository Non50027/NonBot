from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import datetime

# 定義 UserToken 基本模型
class TwitchChannel(SQLModel, table= True):
    id: int = Field(primary_key=True, index=True)
    login: str
    display_name: str= None
    emoji_prefix: str= None
    description: str= None
    icon_url: str= None
    background_url: str= None
    email: str= None
    created_at: datetime
    updated_at: datetime = Field(default_factory=datetime.now, sa_column_kwargs={"onupdate": datetime.now})