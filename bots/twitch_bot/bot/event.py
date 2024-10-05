from bot.tool import CogCore


class Event(CogCore):
    pass
    
def setup(bot):
    bot.add_cog(Event(bot))