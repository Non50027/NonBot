import asyncio, os, uvicorn
from discord_bot import start_bot

# 禁用不安全請求的警告
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


if __name__=="__main__":
    # asyncio.run(start_bot())
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=7615,
    #     reload=True,
        ssl_keyfile=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'key', 'origin.key'),
        ssl_certfile=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'key', 'origin.pem')
    )