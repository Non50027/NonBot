from contextlib import asynccontextmanager
from fastapi import APIRouter, Depends, HTTPException, status
import asyncio, os, discord
from discord_bot import Bot
from ..models import (
    get_session,
    LiveNotifyChannel, LiveNotifyChannelOutput,
    Guild, RoleCreate, Role,
    Channel, 
)
from sqlmodel import Session, select
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder

bot = Bot()

async def init_discord_bot():
    # 啟動 Discord Bot
    loop = asyncio.get_event_loop()
    task = loop.create_task(bot.start(os.getenv('DISCORD_BOT_TOKEN')))
    return task

async def close_discord_bot(task):
    # 停止 Discord Bot
    await bot.close()
    await task
    
router= APIRouter()

# 初始化 Discord Bot 實例
@router.get('/state')
def get_bot_state():
    if bot.is_ready():
        data= {
            'id': bot.user.id,
            'login': bot.user.name,
            'display_name': bot.user.display_name,
            'intents': bot.intents,
            'guilds':[{
                'id': guild.id,
                'name': guild.name,
                'owner_id': guild.owner_id,
                'member_count': guild.member_count,
                'created_at': guild.created_at,
            } for guild in bot.guilds],
            'users': [{
                'id': user.id,
                'name': user.name,
                'display_name': user.display_name,
                'created_at': user.created_at,
            } for user in bot.users],
            'created_at': bot.user.created_at,
        }
        return data
    else: return {'message': 'bot is outline'}
    
@router.post('/sub-twitch/{channel_id}/{twitch_channel_id}')
async def sub_twitch(channel_id: int, twitch_channel_id: int, session: Session= Depends(get_session)):
    # 取得頻道
    temp_channel= bot.get_channel(channel_id)
    # 取得伺服器
    guild= session.get(Guild, temp_channel.guild.id)
    if guild is None: 
        guild= Guild(id= temp_channel.guild.id, name= temp_channel.guild.name)
        session.add(guild)
    
    twitch_channel= session.get(Channel, twitch_channel_id)
    notify_channel= session.exec(select(LiveNotifyChannel).where(LiveNotifyChannel.twitch_channel== twitch_channel)).first()
    if notify_channel and notify_channel.guild== guild:
        notify_channel.id= temp_channel.id
    else:
        notify_channel= LiveNotifyChannel(
            id= temp_channel.id,
            guild= guild,
            twitch_channel= twitch_channel
        )
    session.add(notify_channel)
    session.commit()
    

class NotifyData(BaseModel):
    id: int
    login: str
    display_name: str
    title: str
    game: str
    
@router.get('/notify')
async def notify(data: NotifyData, session: Session= Depends(get_session)):

    data= jsonable_encoder(data)

    embed= discord.Embed()
    embed.title= data['title']
    embed.color= 0x9700d0    #9700d0
    live_url= f"https://www.twitch.tv/{data['login']}"
    embed.url= live_url
    
    img= f"https://static-cdn.jtvnw.net/previews-ttv/live_user_{data['login']}.jpg"
    embed.set_image(url= img)
        
    
    embed.set_author(
            name= data['display_name'],
            url= live_url,
            icon_url= img
            )
    embed.add_field(name= '分類', value= data['game'], inline= False)
    
    # tag= f'<@&{response_data["role"]}>' if response_data['role'] is not None else ''
    twitch_channel= session.get(Channel, data['id'])
    for discord_channel in twitch_channel.discord_channels:
        ch= bot.get_channel(discord_channel.id)
        await ch.send(embed= embed)
        
@router.get('/all-sub/{guild_id}', response_model= list[LiveNotifyChannelOutput])
async def get_all_sub(guild_id: int, session: Session= Depends(get_session)):
    channels= session.exec(select(LiveNotifyChannel).where(LiveNotifyChannel.guild_id== guild_id)).all()
    return channels

