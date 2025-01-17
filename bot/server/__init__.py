import asyncio
from fastapi import FastAPI
from contextlib import asynccontextmanager
from .models import init_db
from .routers import api_discord, api_twitch, oauth
# from ..discord_bot.cmds import role

# Lifespan 管理 FastAPI 的生命週期
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 啟動前的初始化邏輯
    print("初始化資料庫...")
    init_db()  # 初始化資料表
    await asyncio.sleep(1)
    await api_discord.init_discord_bot()
    await asyncio.sleep(5)
    await api_twitch.init_twitch_bot()

    yield  # 等待應用啟動完成

    # 關閉時的清理邏輯
    print("關閉應用：進行清理工作...")
    await api_twitch.close_twitch_bot()
    await api_discord.close_discord_bot()


# 創建 FastAPI 應用，並註冊 lifespan
app = FastAPI(lifespan=lifespan)


app.include_router(router= oauth.router, prefix='/oauth')
app.include_router(router= api_discord.router, prefix='/discord')
# app.include_router(router= role.router, prefix='/discord/reaction')
app.include_router(router= api_twitch.router, prefix='/twitch')
