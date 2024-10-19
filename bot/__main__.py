import asyncio, subprocess, os, uvicorn, requests
from discord_bot import start_bot

# 禁用不安全請求的警告
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


async def main():
    # 同時啟動 Discord 機器人和 FastAPI 伺服器
    await asyncio.gather(
        start_bot()
    )

if __name__=="__main__":
    asyncio.run(start_bot())
    # uvicorn.run(
    #     "discord_bot.server:app",
    #     host="0.0.0.0",
    #     port=7615,
    #     reload=True,
    #     ssl_keyfile=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'key', 'origin.key'),
    #     ssl_certfile=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'key', 'origin.pem')
    # )