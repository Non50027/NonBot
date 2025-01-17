from sqlmodel import Field, SQLModel, Relationship
from . import Channel, ChannelOutput

class RoleBase(SQLModel):
    role_id: int = Field(primary_key=True)
    message_id: int
    emoji_id: int

class Role(RoleBase, table=True):
    # 與 LiveNotifyChannel 一對一關聯
    live_notify_channel_id: int| None= Field(foreign_key= "livenotifychannel.id", unique= True, nullable= False, ondelete= "CASCADE")
    live_notify_channel: "LiveNotifyChannel" = Relationship(back_populates= "role")

class RoleCreate(RoleBase):
    ...
    
class RoleOutput(RoleBase):
    LiveNotifyChannel_id: int

class GuildBase(SQLModel):
    id: int= Field(primary_key= True)
    name: str

class Guild(GuildBase, table= True):
    live_notify_channels: list['LiveNotifyChannel']= Relationship(back_populates= 'guild', cascade_delete= True)

class GuildCreate(GuildBase):
    ...
    
class GuildOutput(GuildBase):
    live_notify_channels: list['LiveNotifyChannelOutput']
    
class LiveNotifyChannelBase(SQLModel):
    id: int= Field(primary_key= True)
    guild_id: str| None= Field(foreign_key= 'guild.id', ondelete= 'CASCADE')
    live_name: str| None= Field(foreign_key= 'channel.login')
    
class LiveNotifyChannel(LiveNotifyChannelBase, table= True):
    guild: Guild= Relationship(back_populates= 'live_notify_channels')
    twitch_channel: Channel= Relationship(back_populates= 'discord_channels')
    
    role: Role| None= Relationship(back_populates= "live_notify_channel")
    
    
class LiveNotifyChannelCreate(LiveNotifyChannelBase):
    ...

class LiveNotifyChannelOutput(LiveNotifyChannelBase):
    ...
    
class LiveNotifyChannelOutputWithTwitch(LiveNotifyChannelOutput):
    twitch_channel: ChannelOutput


