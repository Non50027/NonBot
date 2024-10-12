import os, asyncio, dotenv, requests, urllib3
from bot import Bot

# 忽略 InsecureRequestWarning 警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

dotenv.load_dotenv()

async def main():
    
    print()
    response = requests.get(f"{os.getenv('VITE_BACKEND_DJANGO_URL')}/oauth/check_twitch_token/", verify=False)
    
    if response.status_code!=200:
        response = requests.get(f"{os.getenv('VITE_BACKEND_DJANGO_URL')}/oauth/re_get_twitch_token/", verify=False)
        if response.status_code == 200:
            del os.environ['TWITCH_BOT_TOKEN']
            del os.environ['TWITCH_BOT_REFRESH_TOKEN']
            dotenv.load_dotenv()
        else:
            print(f"刷新 Twitch Token 失敗: {response}")
    
    bot= Bot(
        token= os.getenv('TWITCH_BOT_TOKEN')
    )
    await bot.start()

if __name__=="__main__":
    asyncio.run(main())