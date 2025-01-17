import discord, os, requests, time, httpx, aiohttp, asyncio
from discord.ext import commands
from discord_bot.tool import CogCore, fetch_twitch_data, MyDecorators
from discord import app_commands
from typing import List

class TwitchCmd(CogCore):
    def __init__(self, bot):
        super().__init__(bot)
        self.twitch= {
            'id': os.getenv('VITE_TWITCH_BOT_ID'),
            'token': os.getenv('TWITCH_BOT_TOKEN')
        }
    
    
    @commands.hybrid_command()
    async def ck_twitch_token(self, ctx:commands.Context):
        
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{os.getenv('VITE_BACKEND_DISCORD_URL')}/oauth/validate")
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
        response = requests.get(f"{os.getenv('VITE_BACKEND_DJANGO_URL')}/discord/all_sub/{guild_id}")
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
    
    # @commands.hybrid_command()
    # @commands.is_owner()
    # @app_commands.describe(channel_url= '圖奇頻道網址', channel_id= '要通知的頻道ID')
    # @app_commands.autocomplete(channel_id= channel_choice)
    # async def sub_twitch(self, ctx: commands.Context, channel_url: str, channel_id: str):
    #     '''把指定twitch頻道加入到直播通知列表'''
        
    #     headers = {
    #         'Authorization': f"Bearer {self.twitch['token']}",
    #         'Client-Id': self.twitch['id'],
    #     }
        
    #     channel_name= channel_url.split('twitch.tv/')[1]
    #     # 用 twitch API 獲取頻道基本資料
    #     url= f"https://api.twitch.tv/helix/users?login={channel_name}"
    #     response= requests.get(url, headers=headers)
        
    #     if response.status_code!= 200: 
    #         await ctx.send('頻道搜尋出現錯誤')
            
    #     response_twitch_user_data= response.json()
    #     def find_emoji_prefix(id):
    #         url= f"https://api.twitch.tv/helix/chat/emotes?broadcaster_id={id}"
    #         response= requests.get(url, headers=headers)
    #         if response.status_code== 200:
    #             response_emojis_data= response.json()
    #             emojis= [emoji['name'] for emoji in response_emojis_data['data']]
    #             return os.path.commonprefix(emojis)
    #         else: return None
    #     emoji_prefix= find_emoji_prefix(response_twitch_user_data['data'][0]['id']) if find_emoji_prefix(response_twitch_user_data['data'][0]['id']) else None
    #     new_data={
    #         'guild': ctx.guild.id,
    #         'channel': int(channel_id),
    #         'role': None,
    #         'twitch_channel':{
    #             'id': response_twitch_user_data['data'][0]['id'],
    #             'login': response_twitch_user_data['data'][0]['login'],
    #             'display_name': response_twitch_user_data['data'][0]['display_name'],
    #             'background': response_twitch_user_data['data'][0]['offline_image_url'] or None,
    #             'icon': response_twitch_user_data['data'][0]['profile_image_url'],
    #             'emoji_prefix': emoji_prefix if emoji_prefix is not None else None
    #         },
    #     }
    #     try:
    #         response = requests.post(
    #             f"{os.getenv('VITE_BACKEND_DJANGO_URL')}/discord/sub/",
    #             json= new_data
    #         )
    #         response_data= response.json()
    #         await ctx.send(f"成功將 {response_data['twitch_channel']['display_name']} 直播通知加入 {self.bot.get_channel(int(channel_id)).mention} 頻道")
    #     except Exception as e:
    #         print('requests error', e)
    #         await ctx.send(f'requests error ||{e}||')
    
    # @commands.hybrid_command()
    # async def twitch_emoji(self, ctx):
    #     headers = {
    #         'Authorization': f"Bearer {self.twitch['token']}",
    #         'Client-Id': self.twitch['id'],
    #     }
    #     url= f"https://api.twitch.tv/helix/chat/emotes?broadcaster_id=928328219"
    #     response= requests.get(url, headers=headers)
    #     response_data= response.json()
    #     emojis= [emoji['name'] for emoji in response_data['data']]
    #     prefix= emojis[0]
    #     for emoji in emojis[1:]:
    #         while not emoji.startswith(prefix):
    #             prefix= prefix[:-1]
    #             if prefix== '': return
    
async def setup(bot):
    await bot.add_cog(TwitchCmd(bot))
