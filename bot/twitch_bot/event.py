from twitch_bot.tool import CogCore


class Event(CogCore):
    pass
    
def prepare(bot):
    bot.add_cog(Event(bot))