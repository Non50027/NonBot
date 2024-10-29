from discord_bot.tool import CogCore, restart_task
from discord.ext import tasks, commands
import os, aiohttp, discord, requests
from datetime import datetime

    
class TwitchLiveNotify(CogCore):
    def __init__(self, bot):
        super().__init__(bot)
        self.live_user_id_list= []
        self.user_id= []
        
    async def fetch_data(self, url, headers):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status== 200:
                    response_data= await response.json()
                    return response_data
                elif response.status== 401: return None
    
    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.twitch.wait_for_ready()
        self.bot.discord.loop.create_task(self.start_task())
        
    async def start_task(self):
        restart_task(self.get_user_id)
        restart_task(self.on_live)
    
    @tasks.loop(hours=1)
    async def get_user_id(self):
        response = requests.get(f"{os.getenv('VITE_BACKEND_DJANGO_URL')}/discord/get_all_sub/")
        response_data= response.json()
        self.user_id= '&user_id='.join([_['user_id'] for _ in response_data])
    
    @tasks.loop(seconds= 30)
    async def on_live(self):
        '''偵測直播是否開始'''
        try:
            if self.user_id== []: return
            url= f'https://api.twitch.tv/helix/streams?user_id='+ self.user_id
            headers = {
                'Authorization': f"Bearer {os.getenv('TWITCH_BOT_TOKEN')}",
                'Client-Id': os.getenv('VITE_TWITCH_BOT_ID'),
            }
            live_lists= await self.fetch_data(url, headers)
            
            if live_lists is None: 
                print('live data is None', end='\r')
                return
            
            if not live_lists.get('data'):
                self.live_user_id_list= []
                return
            
            
            await self.bot.twitch.join_channels([_['user_login'] for _ in live_lists['data']]+['infinite0527'])
            
            new_live_user_id_list= list(set([_['user_id'] for _ in live_lists['data']])- set(self.live_user_id_list))
            self.live_user_id_list= [_['user_id'] for _ in live_lists['data']]
            
            for live_data in [_ for _ in live_lists['data'] if _['user_id'] in new_live_user_id_list]:
                
                embed= discord.Embed()
                embed.title= live_data['title']
                embed.color= 0x9700d0    #9700d0
                live_url= f"https://www.twitch.tv/{live_data['user_login']}"
                embed.url= live_url
                
                img= f"https://static-cdn.jtvnw.net/previews-ttv/live_user_{live_data['user_login']}.jpg"
                embed.set_image(url= img)
                    
                response = requests.get(
                    f"{os.getenv('VITE_BACKEND_DJANGO_URL')}/discord/get_sub/", 
                    data= {'user_id': live_data['user_id']}
                    )
                response_data= response.json()
                
                embed.set_author(
                        name= live_data['user_name'],
                        url= live_url,
                        icon_url= response_data['icon_url']
                        )
                embed.add_field(name= '分類', value= live_data['game_name'], inline= False)
                
                tag= f'<@&{response_data["role"]}>' if response_data['role'] is not None else ''
                ch= self.bot.discord.get_channel(int(response_data['channel']))
                await ch.send(tag, embed= embed)
                
                print(f"\033[0;35m{datetime.now().strftime('%H:%M:%S')}\033[0m - \033[0;32m{live_data['user_name']}\033[0m 開台了")
        except Exception as e:
            print('live error', e)
        
    @on_live.before_loop
    async def on_live_is_ready(self):
        '''task 開始前執行'''
        print('     \033[1;32m-\033[0m 開始 twitch live 直播偵測')
    
    @on_live.after_loop
    async def on_live_is_close(self):
        '''task 結束後執行'''
        print('     \033[1;32m-\033[0m 結束 twitch live 直播偵測')


async def setup(bot):
    await bot.add_cog(TwitchLiveNotify(bot))