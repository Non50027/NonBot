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

# 創建一個新的元類，繼承自 discord 和 twitchio 的元類
class CombinedMeta(discord_commands.CogMeta, twitchio_commands.meta.CogMeta):
    pass

# 創建一個新的 Cog 類，同時繼承 discord 和 twitchio 的 Cog
class TestCog(discord_commands.Cog, twitchio_commands.Cog, metaclass=CombinedMeta):
    def __init__(self, bot):
        self.bot = bot