from fastapi import APIRouter, Depends
import asyncio, os, discord
from datetime import datetime, timedelta, timezone
from discord_bot import Bot
from ..models import (
    get_session,
    LiveNotifyChannel, LiveNotifyChannelOutput,
    Guild, Role,
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
    video_id: int
    login: str
    name: str
    title: str
    started_at: str
    viewer_count: int
    game: str
    icon_url: str
    thumbnail_url: str
    background_url: str
    
@router.get('/start-live')
async def start_live(data: NotifyData, session: Session= Depends(get_session)):

    data= jsonable_encoder(data)

    twitch_channel= session.get(Channel, data['id'])

    for discord_channel in twitch_channel.discord_channels:
        ch= bot.get_channel(discord_channel.id)
        if ch is None: continue
        
        live_url= f"https://www.twitch.tv/{data['login']}"
    
        embed= discord.Embed()
        embed.title= data['title']
        embed.color= 0x9700d0    #9700d0
        embed.url= live_url
        embed.set_author(
                name= data['name'],
                url= live_url,
                icon_url= data['icon_url'],
                )
        embed.add_field(name= '分類', value= data['game'], inline= True)
        embed.timestamp= datetime.fromisoformat(data["started_at"])
        embed.set_footer(text= '直播中', icon_url= data['icon_url'])
        
        # 直播中...更新嵌入內容
        if ch.last_message is not None and ch.last_message.embeds[0].timestamp== datetime.fromisoformat(data['started_at']):
            message= ch.last_message
            url= data['thumbnail_url'].format(width= 400, height= 240)
            embed.set_image(url= url)
            embed.add_field(name= "觀看人數", value= data['viewer_count'], inline= True)
            live_time= str(datetime.now(timezone.utc)- datetime.fromisoformat(data['started_at'])).split('.')[0]
            embed.add_field(name= "直播時數", value= live_time, inline= True)
            
            await message.edit(embed= embed)
            
        else: # 新直播
            embed.set_image(url= data['background_url'])
            print(f"\033[0;35m{datetime.now().strftime('%H:%M:%S')}\033[0m - \033[0;32m{data['name']}\033[0m 開台了~")
            await ch.send(embed= embed)
        
class StopLive(BaseModel):
    user_id: int
    # title: str
    # url: str        

@router.get('/stop-live')
async def stop_live(data: StopLive, session: Session= Depends(get_session)):
    
    twitch_channel= session.get(Channel, data.user_id)
    for discord_channel in twitch_channel.discord_channels:
        ch= bot.get_channel(discord_channel.id)
        
        if ch is None: continue
        msg= ch.last_message
        
        if msg is None: continue
        embed= msg.embeds[0]
        
        if embed.footer.text== '直播中':
            print(f"\033[0;35m{datetime.now().strftime('%H:%M:%S')}\033[0m - \033[0;32m{twitch_channel.display_name}\033[0m 關台了~感謝收看~")
            
            embed.set_footer(text= '已結束直播...感謝收看')
            
            view= None
            # if data['title']== embed.title:
            #     view= discord.ui.View()
            #     button= discord.ui.Button(
            #         label= "VOD",
            #         url= data['url']
            #     )
            #     view.add_item(button)
            
            await msg.edit(embed= embed, view= view)
            
        
@router.get('/all-sub/{guild_id}', response_model= list[LiveNotifyChannelOutput])
async def get_all_sub(guild_id: int, session: Session= Depends(get_session)):
    channels= session.exec(select(LiveNotifyChannel).where(LiveNotifyChannel.guild_id== guild_id)).all()
    return channels


@router.post("/role")
async def post_reaction_role(data: Role, session: Session= Depends(get_session)) -> None:
    # data= jsonable_encoder(data)
    db_role= Role.model_validate(data)
    session.add(db_role)
    session.commit()
    
@router.get("/role", response_model= list[Role])
async def get_reaction_role(session: Session= Depends(get_session)):
    data= session.exec(select(Role)).all()
    return data
    
@router.delete("/role/{role_id}")
async def delete_reaction_role(role_id: int, session: Session= Depends(get_session)):
    data= session.get(Role, role_id)
    session.delete(data)
    session.commit()