import os, asyncio, dotenv
from bot import Bot

dotenv.load_dotenv()

async def main():
    
    bot= Bot(
        token= os.getenv('TWITCH_BOT_TOKEN'),
        id= os.getenv('VITE_TWITCH_BOT_ID')
    )
    await bot.start()

if __name__=="__main__":
    asyncio.run(main())