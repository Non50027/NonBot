import discord, os, dotenv, time, urllib3, requests
from datetime import datetime
from discord.ext import commands, tasks
from bot.tool import CogCore, MyDecorators, fetch_twitch_data

# 忽略 InsecureRequestWarning 警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_twitch_token_time():
    response = requests.get(f"{os.getenv('VITE_BACKEND_DJANGO_URL')}/oauth/check_twitch_token/", verify=False)
    response_data= response.json()
    
    return response_data['expires_in'] if response.status_code==200 else 300

class TwitchTask(CogCore):
    def __init__(self, bot):
        super().__init__(bot)
        self.twitch= {
            'id': os.getenv('VITE_TWITCH_BOT_ID'),
            'token': os.getenv('TWITCH_BOT_TOKEN'),
            'time': get_twitch_token_time()
        }
        self.live_user_id_list= []
        self.user_id= []
    
    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.loop.create_task(self.start_task_init())
    
    def restart_or_start(self, func):
        if func.is_running():
            func.restart()
        else:
            func.start()
    
    async def start_task_init(self):
        self.restart_or_start(self.get_sub_user_id)
        self.restart_or_start(self.on_live)
        self.restart_or_start(self.loop_check_twitch_token)
    
    @tasks.loop(hours=1)
    async def get_sub_user_id(self):
        response = requests.get(f"{os.getenv('VITE_BACKEND_DJANGO_URL')}/discord/get_all_sub/", verify=False)
        response_data= response.json()
        self.user_id= '&user_id='.join([_['user_id'] for _ in response_data])
    
    @commands.hybrid_command()
    async def stop_task(self, ctx: commands.Context):
        self.loop_check_twitch_token.stop()
        await ctx.send('結束 twitch token 偵測任務')
    
    @commands.hybrid_command()
    @commands.is_owner()
    async def restart_all_task(self, ctx: commands.Context):
        '''重新啟動任務'''
        self.get_sub_user_id.restart()
        self.on_live.restart()
        self.loop_check_twitch_token.restart()
        print('   \033[1;32m-\033[0m 重新開始偵測任務')
        await ctx.send('重新開始偵測任務')
    
    @tasks.loop(minutes=5)
    async def loop_check_twitch_token(self):
        '''檢查 token 並重新獲取'''
        self.twitch['time'] -= 300  # 每次檢查後剩餘時間減少60秒（1分鐘）

        # 如果剩餘時間小於5分鐘，則刷新Token
        if self.twitch['time'] <= 300:  # 300秒 = 5分鐘
            try:
                print(f"刷新 Twitch Token ... ")
                response = requests.get(f"{os.getenv('VITE_BACKEND_DJANGO_URL')}/oauth/re_get_twitch_token/", verify=False)
                response_data= response.json()
                if response.status_code == 200:
                    del os.environ['TWITCH_BOT_TOKEN']
                    del os.environ['TWITCH_BOT_REFRESH_TOKEN']
                    dotenv.load_dotenv()
                    self.twitch['time'] = response_data['expires_in']  # 更新新的有效期
                    print(f"Twitch Token 刷新成功 ... 有效期限至: {time.strftime('%H: %M: %S', time.localtime( time.time()+ self.twitch['time']))}")
                else:
                    print(f"刷新 Twitch Token 失敗: {response}")
            except Exception as e:
                print('error', e)
    
    @loop_check_twitch_token.before_loop
    async def loop_check_twitch_token_is_ready(self):
        '''task 開始前執行'''
        await self.bot.wait_until_ready()
        print('     \033[1;32m-\033[0m 開始 Twitch Bot Token 偵測')
    
    @loop_check_twitch_token.after_loop
    async def loop_check_twitch_token_is_close(self):
        '''task 結束後執行'''
        print('     \033[1;32m-\033[0m 結束 Twitch Bot Token 偵測')
    
    @tasks.loop(seconds= 30)
    async def on_live(self):
        '''偵測直播是否開始'''
        headers = {
            'Authorization': f"Bearer {os.getenv('TWITCH_BOT_TOKEN')}",
            'Client-Id': self.twitch['id'],
        }
        url= f'https://api.twitch.tv/helix/streams?user_id='+ self.user_id
        live_lists= await fetch_twitch_data(url, headers)
        if live_lists['data']== []:
            self.live_user_id_list= []
            return
        
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
                
            response = requests.get(f"{os.getenv('VITE_BACKEND_DJANGO_URL')}/discord/get_sub/", data= {'user_id': live_data['user_id']}, verify=False)
            response_data= response.json()
            
            embed.set_author(
                    name= live_data['user_name'],
                    url= live_url,
                    icon_url= response_data['icon_url']
                    )
            embed.add_field(name= '分類', value= live_data['game_name'], inline= False)
            
            
            tag= f'<@&{response_data["role"]}>' if response_data['role'] is not None else ''
            ch= self.bot.get_channel(int(response_data['channel']))
            try:
                await ch.send(tag, embed= embed)
            except Exception as e:
                print('send error', e)
            
            print(f"\033[0;35m{datetime.now().strftime('%H:%M:%S')}\033[0m - \033[0;32m{live_data['user_name']}\033[0m 開台了")
        
    @on_live.before_loop
    async def on_live_is_ready(self):
        '''task 開始前執行'''
        await self.bot.wait_until_ready()
        print('     \033[1;32m-\033[0m 開始 直播偵測')
    
    @on_live.after_loop
    async def on_live_is_close(self):
        '''task 結束後執行'''
        print('     \033[1;32m-\033[0m 結束 直播偵測')

async def setup(bot):
    await bot.add_cog(TwitchTask(bot))
