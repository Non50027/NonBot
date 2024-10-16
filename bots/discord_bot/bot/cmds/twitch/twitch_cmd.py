import discord, os, requests, time
from discord.ext import commands
from bot.tool import CogCore, fetch_twitch_data, MyDecorators
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
        
        response = requests.get(f"{os.getenv('VITE_BACKEND_DJANGO_URL')}/oauth/check_twitch_token/", verify=False)
        response_data= response.json()
        
        if response.status_code==200:
            msg= f"twitch token OK\n登入帳號：{response_data['login']}\n權限範圍：{', '.join(response_data['scopes'])}\n剩餘時間：{time.strftime('%H: %M: %S', time.gmtime((response_data['expires_in'])))}"
        else:
            msg= f"twitch token 失效 {response_data['status']}, {response_data['message']}"
        await ctx.send(msg, ephemeral= True)
    
    @commands.hybrid_command()
    @MyDecorators.readJson('test')
    async def show_sub(self, ctx: commands.Context):
        response = requests.get(f"{os.getenv('VITE_BACKEND_DJANGO_URL')}/discord/get_all_sub/", verify=False)
        response_data= response.json()
        return response_data
    
    @commands.hybrid_command()
    @MyDecorators.readJson('subLive')
    async def is_live(self, ctx: commands.Context):
        '''顯示正在直播'''
        headers = {
            'Authorization': f"Bearer {self.twitch['token']}",
            'Client-Id': self.twitch['id'],
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
    
    # 頻道清單
    async def channel_choice(self, interaction: discord.Interaction, current: str) -> List[app_commands.Choice[str]]:
        return [app_commands.Choice(name= ch.name, value= str(ch.id)) for ch in interaction.guild.channels][:25]
    
    @commands.hybrid_command()
    @commands.is_owner()
    @app_commands.describe(channel_url= '圖奇頻道網址', channel_id= '要通知的頻道ID')
    @app_commands.autocomplete(channel_id= channel_choice)
    async def sub_twitch(self, ctx: commands.Context, channel_url: str, channel_id: str):
        '''把指定twitch頻道加入到直播通知列表'''
        
        headers = {
            'Authorization': f"Bearer {self.twitch['token']}",
            'Client-Id': self.twitch['id'],
        }
        
        channel_name= channel_url.split('twitch.tv/')[1]
        # 用 twitch API 獲取頻道基本資料
        url= f"https://api.twitch.tv/helix/users?login={channel_name}"
        response= requests.get(url, headers=headers)
        response_data= response.json()
        
        if not response_data['data']: 
            await ctx.send('查無頻道')
            return self.json_data
        new_data={
            'guild': ctx.guild.id,
            'user_id': response_data['data'][0]['id'],
            'user_login': response_data['data'][0]['login'],
            'user_name': response_data['data'][0]['display_name'],
            'channel': channel_id,
            'role': None,
            'background_url': response_data['data'][0]['offline_image_url'],
            'icon_url': response_data['data'][0]['profile_image_url'],
            'on_live': False,
        }
        try:
            response = requests.post(f"{os.getenv('VITE_BACKEND_DJANGO_URL')}/discord/sub/",data= new_data, verify=False)
            
            response_data= response.json()
            
            print(response_data)
        except Exception as e:
            print('requests error', e)
    
async def setup(bot):
    await bot.add_cog(TwitchCmd(bot))
