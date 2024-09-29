import os, asyncio, dotenv
from bot import Bot

    
async def main():
    
    bot= Bot()
    
    dotenv.load_dotenv()
    await bot.start(os.getenv('DISCORD_BOT_TOKEN'))
    
if __name__=="__main__":
    asyncio.run(main())