from discord.ext import commands
from discord.ext import commands as discord_commands
from twitchio.ext import commands as twitchio_commands

class CogCore(commands.Cog):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot= bot
    
    async def get_ctx(self):
        ch= self.bot.get_channel(656791892440121354)
        msg= await ch.fetch_message(1289805561952600126)
        ctx= await self.bot.get_context(msg)
        return ctx
