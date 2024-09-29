from discord.ext import commands

class CogCore(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot= bot
        super().__init__()