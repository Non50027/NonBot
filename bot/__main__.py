import urllib3, asyncio, subprocess, os, uvicorn
from discord_bot import start_bot#, start_server

# 忽略 InsecureRequestWarning 警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
async def start_server():
    # subprocess.Popen(
    #     [
    #         "uvicorn",
    #         "discord_bot.server:app",
    #         "--host",
    #         "0.0.0.0",
    #         "--port", 
    #         "7615", 
    #         "--reload",
    #         f"--ssl-keyfile={os.path.join(os.path.dirname(os.path.dirname(__file__)), 'non.com.tw.key')}",
    #         f"--ssl-certfile={os.path.join(os.path.dirname(os.path.dirname(__file__)), 'non.com.tw.pem')}"
    #     ],
    # )
    config = uvicorn.Config(
        "discord_bot.server.request:app",  # "main" 是指這個文件，"app" 是 FastAPI 實例名稱
        host='61.63.220.46',
        port=7615,
        reload=True,
        reload_dirs= [os.path.join(os.path.dirname(__file__), 'discord_bot', 'server')],
        ssl_keyfile=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'non.com.tw.key'),
        ssl_certfile=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'non.com.tw.pem')
    )
    server = uvicorn.Server(config)
    await server.serve()
    
async def main():
    # 同時啟動 Discord 機器人和 FastAPI 伺服器
    await asyncio.gather(
        start_bot(),
        start_server()
    )
    
if __name__=="__main__":
    asyncio.run(start_bot())