from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .db_discord import LiveNotifyChannel, LiveNotifyChannelOutput

class ChannelBase(SQLModel):
    id: int = Field(primary_key=True, index=True)
    login: str= Field(index= True)
    display_name: str| None= None
    description: str| None= None
    icon_url: str| None= None
    background_url: str| None= None
    email: str| None= None
    created_at: datetime
    emoji_prefix: str| None= Field(default= None)
    updated_at: datetime = Field(default_factory=datetime.now, sa_column_kwargs={"onupdate": datetime.now})

class Channel(ChannelBase, table= True):
    # 與 UserToken 的關聯
    token: "Token" = Relationship(back_populates="channel", cascade_delete= True)
    # 與 Emoji Item 的關聯
    emojis: list["Emoji"] = Relationship(back_populates="channel", cascade_delete= True)
    
    discord_channels: list["LiveNotifyChannel"]| None= Relationship(back_populates= "twitch_channel", cascade_delete= True)
    
class ChannelCreate(ChannelBase):
    emojis: list["Emoji"]
    
class ChannelOutput(ChannelBase):
    emojis: list['Emoji']| None
    
class ChannelOutputWithDiscord(ChannelOutput):
    discord_channels: list['LiveNotifyChannelOutput']

class ChannelUpdate(ChannelBase):
    display_name: str| None= None
    description: str| None= None
    icon_url: str| None= None
    background_url: str| None= None
    email: str| None= None
    emoji_prefix: str| None= None
    emojis: list["EmojiCreate"]| None= None

class EmojiBase(SQLModel):
    id: str= Field(primary_key=True, index=True)
    name: str= Field(index= True)
    tier: str
    image_1x_url: str
    image_4x_url: str
    prefix: str|None = Field(foreign_key="channel.emoji_prefix", ondelete='CASCADE')

class Emoji(EmojiBase, table= True):
    # 與 Twitch Channel 的關聯
    channel: Channel = Relationship(back_populates="emojis")
    
class EmojiCreate(EmojiBase):
    ...
    
class EmojiOutput(EmojiBase):
    ...
    
class TokenBase(SQLModel):
    id: str = Field(primary_key=True, foreign_key="channel.id", index=True, ondelete='CASCADE')
    access_token: str
    refresh_token: str
    scopes: str
    expires_at: datetime
    updated_at: datetime = Field(default_factory=datetime.now, sa_column_kwargs={"onupdate": datetime.now})
    
# 定義 Token 基本模型
class Token(TokenBase, table= True):
    # 外鍵連接 Channel
    channel: Channel= Relationship(back_populates= 'token')
    
class TokenCreate(TokenBase):
    ...

class TokenOutput(TokenBase):
    ...