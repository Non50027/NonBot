from fastapi import FastAPI, Depends
from discord_bot import Bot
import os, asyncio
from contextlib import asynccontextmanager

discord_bot: Bot= None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global discord_bot
    discord_bot = Bot()

    # 2. 啟動 Discord Bot
    loop = asyncio.get_event_loop()
    task = loop.create_task(discord_bot.start(os.getenv('DISCORD_BOT_TOKEN')))
    
    yield  # FastAPI 應用啟動後執行

    # 3. 停止 Discord Bot
    await discord_bot.close()
    await task

# 4. 建立 FastAPI 應用並設置 lifespan
app = FastAPI(lifespan= lifespan)

@app.get('/')
async def home():
    print('home')
    return {'message': 'OK...'}

@app.get('/get_guilds')
async def get_name():
    print(discord_bot.guilds)
    return {'message': 'OK'}

# 初始化 Discord Bot 實例
@app.get('/get_bot')
def get_discord_bot():
    print('server to discord bot', )
    return {'discord bot': 'ok'}