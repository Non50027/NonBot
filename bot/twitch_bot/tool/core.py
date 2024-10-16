from twitchio.ext import commands
import os

class CogCore(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot= bot
        # load .env file
        # dotenv.load_dotenv()
        self.token= os.getenv('TWITCH_BOT_TOKEN'),
        self.id= os.getenv('VITE_TWITCH_BOT_ID')
    