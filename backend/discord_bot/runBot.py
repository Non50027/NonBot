import os, dotenv, asyncio
from bot import Bot

dotenv.load_dotenv()

async def main():

    
    bot= Bot()
    await bot.start(os.getenv('DISCORD_BOT_TOKEN'))

if __name__=="__main__":
    asyncio.run(main())