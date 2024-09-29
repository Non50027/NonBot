import discord, os, requests
from discord.ext import commands
from typing import List
from discord import app_commands
from bot.tool import CogCore, MyDecorators, fetch_twitch_data

class Live(CogCore):
    def __init__(self, bot):
        super().__init__(bot)
        self.twitch_id= os.getenv('VITE_TWITCH_BOT_ID')
        
    # 頻道清單
    async def channel_choice(self, interaction: discord.Interaction, current: str) -> List[app_commands.Choice[str]]:
        return [app_commands.Choice(name= ch.name, value= str(ch.id)) for ch in interaction.guild.channels][:25]
    
    @commands.command()
    async def meg(self, ctx):
        print('OK')
    
    @commands.hybrid_command()
    @MyDecorators.readJson('subLive')
    async def on_live(self, ctx: commands.Context):
        headers = {
            'Authorization': f"Bearer {os.getenv('TWITCH_BOT_TOKEN')}",
            'Client-Id': self.twitch_id,
        }
        url= f'https://api.twitch.tv/helix/streams?user_id='
        msg=[]
        for sub_channels in self.json_data.values():
            subUser_id= [_['id'] for _ in sub_channels['twitch']]
            user_id= '&user_id='.join(subUser_id)
            try:
                live_lists= await fetch_twitch_data(url+user_id, headers)
            except Exception as e:
                print('on_live error ', e)
                return
            
            for sub_channel in sub_channels['twitch']:
                
                # 未在直播
                if sub_channel['id'] not in [_['user_id'] for _ in live_lists['data']]:
                    sub_channel['live']= 'False'
                    continue
                
                # 加上直播中標籤
                sub_channel['live']= 'True'
                
                live_data= [_ for _ in live_lists['data'] if _['user_id']== sub_channel['id']][0]
                live_url= f"https://www.twitch.tv/{live_data['user_login']}"
                msg.append(f" ### {live_data['user_name']} \t [{live_data['title']}](<{live_url}>)")
                
        await ctx.send('\n'.join(msg))
        return self.json_data
    
    @commands.hybrid_command()
    @commands.is_owner()
    @app_commands.describe(channel_url= '圖奇頻道網址', channel_id= '要通知的頻道ID')
    @app_commands.autocomplete(channel_id= channel_choice)
    @MyDecorators.readJson('subLive')
    async def sub_twitch(self, ctx: commands.Context, channel_url: str, channel_id: str):
        '''
        把指定twitch頻道加入到直播通知列表
        '''
        headers = {
            'Authorization': f"Bearer {os.getenv('TWITCH_BOT_TOKEN')}",
            'Client-Id': self.twitch_id,
        }
        channel_name= channel_url.split('twitch.tv/')[1]
        # 初始化伺服器資料
        if ctx.guild.name not in self.json_data:
            self.json_data[ctx.guild.name]= {}
            
        if 'twitch' not in self.json_data[ctx.guild.name]:
            self.json_data[ctx.guild.name]['twitch']= []
            
        # 用 twitch API 獲取頻道基本資料
        url= f"https://api.twitch.tv/helix/users?login={channel_name}"
        r= requests.get(url, headers=headers)
        chData= r.json()
        
        if not chData['data']: 
            await ctx.send('查無頻道')
            return self.json_data
            
        # 格式化資料
        chData={
            'id': chData['data'][0]['id'],
            'name': chData['data'][0]['login'],
            'display_name': chData['data'][0]['display_name'],
            'icon_url': chData['data'][0]['profile_image_url'],
            'background_url': chData['data'][0]['offline_image_url'],
            'channel': int(channel_id),
            'live': 'False',
            'role': None,
        }
        # print(chData)
        # 加入資料
        self.json_data[ctx.guild.name]['twitch'].append(chData)
        ch= self.bot.get_channel(int(channel_id))
        await ctx.channel.send(f"成功將 `{chData['display_name']}` 直播通知加入 {ch.mention} 頻道")
        
        return self.json_data

async def setup(bot):
    await bot.add_cog(Live(bot))
