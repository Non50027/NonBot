import discord, os, requests, time, httpx, aiohttp, asyncio
from discord.ext import commands
from discord_bot.tool import CogCore, fetch_twitch_data, MyDecorators
from discord import app_commands
from typing import List

class TwitchCmd(CogCore):
    def __init__(self, bot):
        super().__init__(bot)
        self.twitch= {
            'id': os.getenv('TWITCH_BOT_ID'),
            'token': os.getenv('TWITCH_BOT_TOKEN')
        }
    
    
    @commands.hybrid_command()
    @commands.is_owner()
    async def ck_twitch_token(self, ctx:commands.Context):
        
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{os.getenv('BACKEND_URL')}/oauth/validate")
        response_data= response.json()
        
        if response.status_code==200:
            msg= f"twitch token OK\n登入帳號：{response_data['login']}\n權限範圍：{', '.join(response_data['scopes'])}\n有效期限至：{time.strftime('%H: %M: %S', time.localtime(time.time()+ response_data['expires_in']))}"
        else:
            print(response.status_code, response_data)
            msg= f"twitch token 失效 {response_data['status']}, {response_data['message']}"
        await ctx.send(msg, ephemeral= True)
    
    @commands.hybrid_command()
    async def show_sub(self, ctx: commands.Context):
        guild_id= ctx.guild.id
        response = requests.get(f"{os.getenv('BACKEND_URL')}/discord/all_sub/{guild_id}")
        response_data= response.json()
        print(response_data)
    
    async def fetch_data(self, url, headers):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                response_data= await response.json()
                if response.status== 200:
                    return response_data
                elif response.status== 401: 
                    print('live data is None', response_data, end='\r')
                    return None
    
    
    # 頻道清單
    async def channel_choice(self, interaction: discord.Interaction, current: str) -> List[app_commands.Choice[str]]:
        return [app_commands.Choice(name= ch.name, value= str(ch.id)) for ch in interaction.guild.channels][:25]

    
async def setup(bot):
    await bot.add_cog(TwitchCmd(bot))
