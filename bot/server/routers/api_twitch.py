import asyncio, os, time, dotenv, requests
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from twitch_bot import Bot
from ..models import get_session, Channel, Emoji, ChannelOutput, ChannelOutputWithEmoji
from sqlmodel import Session, select
from ..tool import update_env_variable

def check_twitch_token():
    '''檢查 token 並重新獲取'''
    url= 'https://id.twitch.tv/oauth2/validate'
    
    headers = {'Authorization': f"Bearer {os.getenv('TWITCH_BOT_TOKEN')}"}  
    
    response= requests.get(url, headers= headers)
    response_data= response.json()
    
    if response.status_code==200: return
    
    print(f"\033[0;35m{datetime.now().strftime('%H:%M:%S')}\033[0m - 刷新 Twitch Token ... ")
    
    url= 'https://id.twitch.tv/oauth2/token'
    
    headers={'Content-Type': 'application/x-www-form-urlencoded'}
    
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': os.getenv('TWITCH_BOT_REFRESH_TOKEN'),
        'client_id': os.getenv('VITE_TWITCH_BOT_ID'),
        'client_secret': os.getenv('TWITCH_BOT_SECRET'),
    }
    response= requests.post(url, headers= headers, data= data)
    response_data= response.json()
    
    if response.status_code== 200:
        response_data= response.json()
        update_env_variable('TWITCH_BOT_TOKEN', response_data['access_token'])
        update_env_variable('TWITCH_BOT_REFRESH_TOKEN', response_data['refresh_token'])
        # 在重新加載前，手動刪除舊的環境變數
        del os.environ['TWITCH_BOT_TOKEN']
        del os.environ['TWITCH_BOT_REFRESH_TOKEN']
        dotenv.load_dotenv()
        print(f"Twitch Token 刷新成功 ... ")
        print(f"有效時間至: \033[0;35m{time.strftime('%H: %M: %S', time.localtime( time.time()+ response_data['expires_in']))}\033[0m")
    else:
        print('刷新 Twitch Token 失敗', response_data['status'], response_data['error'], response_data['message'])

check_twitch_token()

bot = Bot(
    token= os.getenv('TWITCH_BOT_TOKEN'),
    secret= os.getenv('TWITCH_BOT_SECRET')
)

async def init_twitch_bot():
    # 啟動 Twitch Bot
    loop = asyncio.get_event_loop()
    task = loop.create_task(bot.start())
    return task

async def close_twitch_bot(task):
    # 停止 Twitch Bot
    await bot.close()
    await task

router= APIRouter()

# 取得 twitch Bot 狀態
@router.get('/state')
async def get_state():
    await bot.wait_for_ready()
    data= {
        'id': bot.user_id,
        'login': bot.nick,
        'channels':[channel.name for channel in bot.connected_channels]
    }
    
    return data

@router.get("/reload")
async def reload_cog():
    bot.reload_cog()

@router.get('/all-sub-channel', response_model= list[ChannelOutput])
async def get_channel(session: Session = Depends(get_session)):
    channels = session.exec(select(Channel)).all()
    return channels

@router.get('/channel/{id}', response_model= ChannelOutput)
async def fetch_channel(id: int, session: Session = Depends(get_session)):
    channel = session.get(Channel, id)
    if channel in None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= "沒有資料")
    return channel


@router.post('/channel/{name}', response_model= ChannelOutputWithEmoji)
async def create_channel(name: str, session: Session = Depends(get_session)):
    # 取得使用者資料
    users= await bot.fetch_users(names= [name])
    user= users[0]
    
    # 檢查是否已有資料
    channel= session.get(Channel, user.id)
    # 如果有資料
    if channel: return channel
    
    # 取得頻道資料
    ch= await bot.fetch_channel(name)
    # 取得表符列表
    emojis= await ch.user.fetch_channel_emotes()
    # 表符前綴
    emoji_prefix= None if emojis== [] else os.path.commonprefix([_.name for _ in emojis])
    
    # 建立資料庫物件
    new_channel = Channel(id= user.id, login= user.name, created_at= user.created_at)
    new_channel.display_name= user.display_name
    new_channel.description= user.description
    new_channel.icon_url= user.profile_image
    new_channel.background_url= user.offline_image
    new_channel.email= user.email
    # 如果該頻道有自訂表符
    if emoji_prefix is not None:
        new_channel.emoji_prefix= emoji_prefix
        new_channel.emojis= [
            Emoji(
                id= emoji.id,
                name= emoji.name,
                tier= emoji.tier,
                image_1x_url= emoji.images['url_1x'],
                image_4x_url= emoji.images['url_4x'],
            ) 
        for emoji in emojis
        ]
    session.add(new_channel)
    session.commit()
        
    return new_channel

@router.put('/channel/{name}', response_model= ChannelOutput)
async def update_channel(name: str, session: Session = Depends(get_session)):
    # 取得使用者資料
    users= await bot.fetch_users(names= [name])
    user= users[0]
    # 檢查是否已有資料    
    channel= session.get(Channel, user.id)
    # 沒有資料
    if channel is None: raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= "沒有資料")
    
    # 取得頻道資料
    ch= await bot.fetch_channel(name)
    # 取得表符列表
    emojis= await ch.user.fetch_channel_emotes()    
    # 表符前綴
    emoji_prefix= None if emojis== [] else os.path.commonprefix([_.name for _ in emojis])    
    
    
    # 建立資料庫物件
    update_data= Channel()
    update_data.display_name= user.display_name
    update_data.description= user.description
    update_data.icon_url= user.profile_image
    update_data.background_url= user.offline_image
    update_data.email= user.email
    
    # 如果該頻道有自訂表符
    if emoji_prefix is not None:
        # 刪除舊的表符
        before_emojis= session.exec(select(Emoji).where(Emoji.prefix== channel.emoji_prefix)).all()
        for before_emoji in before_emojis:
            session.delete(before_emoji)
        # 新的表符
        update_data.emoji_prefix= emoji_prefix
        update_data.emojis= [
            Emoji(
                id= emoji.id,
                name= emoji.name,
                tier= emoji.tier,
                image_1x_url= emoji.images['url_1x'],
                image_4x_url= emoji.images['url_4x'],
            ) 
        for emoji in emojis
        ]
        
    channel.sqlmodel_update(update_data.model_dump(exclude_unset= True))
    session.add(channel)
    session.commit()
            
    return channel
    
@router.delete('/channel/{id}')
async def delete_channel(id: int, session: Session= Depends(get_session)):
    channel= session.get(Channel, id)
    session.delete(channel)
    session.commit()
    # emoji= session.exec(select(Emoji).where(Emoji.prefix== channel.emoji_prefix)).all()
