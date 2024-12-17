from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import datetime

# 定義 UserToken 基本模型
class UserToken(SQLModel, table= True):
    user_id: int = Field(primary_key=True, index=True)  # Twitch 使用者 ID
    access_token: str
    refresh_token: str
    scopes: Optional[str] = None  # 授權範圍，使用逗號分隔的字串
    expires_at: datetime
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now, sa_column_kwargs={"onupdate": datetime.now})