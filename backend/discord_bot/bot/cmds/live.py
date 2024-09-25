import discord, json, os, requests, dotenv, aiohttp
from discord.ext import commands
from bot.decrators import MyDecorators
from bot.serve import fetch_twitch_data

dotenv.load_dotenv()

class Live(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()
    
    @commands.hybrid_command()
    @MyDecorators.readJson('subLive')
    async def on_live(self, ctx: commands.Context):
        headers = {
            'Authorization': f"Bearer {os.getenv('TWITCH_BOT_TOKEN')}",
            'Client-Id': os.getenv('VITE_TWITCH_BOT_ID'),
        }
        url= f'https://api.twitch.tv/helix/streams?user_id='
        msg=[]
        for subChannels in self.data.values():
            subUserId= [_['id'] for _ in subChannels['twitch']]
            userId= '&user_id='.join(subUserId)
            try:
                liveLists= await fetch_twitch_data(url+userId, headers)
            except Exception as e:
                print('on_live error ', e)
                return
            
            for subChannel in subChannels['twitch']:
                
                # 未在直播
                if subChannel['id'] not in [_['user_id'] for _ in liveLists['data']]:
                    subChannel['live']= 'False'
                    continue
                
                # 加上直播中標籤
                subChannel['live']= 'True'
                
                liveData= [_ for _ in liveLists['data'] if _['user_id']== subChannel['id']][0]
                liveUrl= f"https://www.twitch.tv/{liveData['user_login']}"
                msg.append(f" ### {liveData['user_name']} \t [{liveData['title']}](<{liveUrl}>)")
                
        await ctx.send('\n'.join(msg))
        return self.data

async def setup(bot):
    await bot.add_cog(Live(bot))
