
import asyncio, os, requests
from contextlib import asynccontextmanager
from fastapi import APIRouter
from twitch_bot import Bot


# twitch_bot: Bot= None
bot = Bot(
    token= os.getenv('TWITCH_BOT_TOKEN'),
    secret= os.getenv('TWITCH_BOT_SECRET')
)

@asynccontextmanager
async def lifespan(app: APIRouter):
    global bot

    # 2. 啟動 twitch Bot
    loop = asyncio.get_event_loop()
    task = loop.create_task(bot.start())
    
    yield  # FastAPI 應用啟動後執行

    # 3. 停止 twitch Bot
    await bot.close()
    await task

header = {
    'Client-ID': os.getenv('VITE_TWITCH_BOT_ID'),
    'Authorization': f"Bearer {os.getenv('TWITCH_BOT_TOKEN')}"
}

router= APIRouter(lifespan= lifespan)

@router.get('/get-user')
async def get_user(name: str= None):
    if name is not None: name= [name]
    users= await bot.fetch_users(names= name)
    data= [
        {
            'id': user.id,
            'login': user.name,
            'display_name': user.display_name,
            'description': user.description,
            'icon_url': user.profile_image,
            'background_url': user.offline_image,
            'email': user.email,
            'created_at': user.created_at,
        } for user in users
    ]
    return data

@router.get('/get-channel')
async def get_channel(q: str):
    ch= await bot.fetch_channel(q)
    ch_data= {
        'user': ch.user.name,
        'title': ch.title,
        'game': ch.game_name,
        'tag': ch.tags,
    }
    emoji= await ch.user.fetch_channel_emotes()
    emojis= [
        {
            'name': e.name,
            'tier': e.tier
        } for e in emoji
    ]
    ch_data['emojis']= emojis
    return ch_data

    
# 取得 twitch Bot 狀態
@router.get('/get-bot-state')
async def get_bot_state():
    await bot.wait_for_ready()
    data= {
        'id': bot.user_id,
        'login': bot.nick
    }
    return data

