
from contextlib import asynccontextmanager
from fastapi import APIRouter
import asyncio, os
from discord_bot import Bot


# discord_bot: Bot= None
bot = Bot()

@asynccontextmanager
async def lifespan(app: APIRouter):
    global bot

    # 2. 啟動 Discord Bot
    loop = asyncio.get_event_loop()
    task = loop.create_task(bot.start(os.getenv('DISCORD_BOT_TOKEN')))
    
    yield  # FastAPI 應用啟動後執行

    # 3. 停止 Discord Bot
    await bot.close()
    await task

router= APIRouter(lifespan= lifespan)

@router.get('/get_guilds')
async def get_guilds():
    data= [{
        'id': guild.id,
        'name': guild.name,
        'description': guild.description,
        'channels_count': len(guild.channels),
        'members_count': guild.member_count or len(guild.members),
        'owner': {
            'login': guild.owner.name,
            'dispaly_name': guild.owner.display_name,
        },
    } for guild in bot.guilds]
    return data

# 初始化 Discord Bot 實例
@router.get('/get-bot-state')
def get_bot_state():
    if bot.is_ready():
        data= {
            'id': bot.user.id,
            'login': bot.user.name,
            'display_name': bot.user.display_name,
            'created_at': bot.user.created_at,
            'guilds':[{
                'id': guild.id,
                'name': guild.name,
            } for guild in bot.guilds],
        }
        return data
    else: return {'message': 'bot is outline'}