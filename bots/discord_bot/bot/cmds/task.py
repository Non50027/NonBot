import discord, requests, os, urllib3, time, dotenv
from datetime import datetime
from discord.ext import tasks, commands
from bot.tool import CogCore, fetch_twitch_data, MyDecorators

# 忽略 InsecureRequestWarning 警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Task(CogCore):
    def __init__(self, bot):
        super().__init__(bot)
        self.twitch= {
            'id': os.getenv('VITE_TWITCH_BOT_ID'),
            'time': self.get_twitch_token_time()
        }
        self.bot.loop.create_task(self.start_task_init())
        
    def get_twitch_token_time(self):
        response = requests.get(f"{os.getenv('VITE_BACKEND_DJANGO_URL')}/oauth/check_twitch_token/", verify=False)
        response_data= response.json()
        
        return response_data['expires_in'] if response.status_code==200 else 300
        
    async def start_task_init(self):
        await self.bot.wait_until_ready()
        self.on_live.start()
        self.loop_check_twitch_token.start()
    
    @commands.hybrid_command()
    @commands.is_owner()
    async def restart_all_task(self, ctx: commands.Context):
        self.on_live.restart()
        self.loop_check_twitch_token.restart()
        print('   \033[1;32m-\033[0m 重新開始偵測任務')
        await ctx.send('重新開始偵測任務')
    
    @tasks.loop(minutes=5)
    async def loop_check_twitch_token(self):
        
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
                    print(f"Twitch Token 刷新成功 ... 新的時間為 {time.strftime('%H: %M: %S', time.gmtime(self.twitch['time']))} sec")
                else:
                    print(f"刷新 Twitch Token 失敗: {response}")
            except Exception as e:
                print('error', e)
    
    @loop_check_twitch_token.before_loop
    async def loop_check_twitch_token_is_ready(self):
        await self.bot.wait_until_ready()
        print('     \033[1;32m-\033[0m 開始 Twitch Bot Token 偵測')
        
    @tasks.loop(seconds= 30)
    @MyDecorators.readJson('subLive')
    async def on_live(self):
        
        headers = {
            'Authorization': f"Bearer {os.getenv('TWITCH_BOT_TOKEN')}",
            'Client-Id': self.twitch['id'],
        }
        url= f'https://api.twitch.tv/helix/streams?user_id='
            
        for sub_channels in self.json_data.values():
            sub_user_id= [_['id'] for _ in sub_channels['twitch']]
            user_id= '&user_id='.join(sub_user_id)
            try:
                live_lists= await fetch_twitch_data(url+ user_id, headers)
            except Exception as e:
                print('on_live error ', e)
                return
            
            for sub_channel in sub_channels['twitch']:
                
                # 未在直播
                if sub_channel['id'] not in [_['user_id'] for _ in live_lists['data']]:
                    sub_channel['live']= 'False'
                    continue
                    
                # 已有開始直播的標籤...避免重複通知
                if sub_channel['live']== 'True':
                    continue
                
                # 加上直播中標籤
                sub_channel['live']= 'True'
                
                live_data= [_ for _ in live_lists['data'] if _['user_id']== sub_channel['id']][0]
                
                embed= discord.Embed()
                embed.title= live_data['title']
                embed.color= 0x9700d0    #9700d0
                live_url= f"https://www.twitch.tv/{live_data['user_login']}"
                embed.url= live_url
                
                img= f"https://static-cdn.jtvnw.net/previews-ttv/live_user_{live_data['user_login']}.jpg"
                embed.set_image(url= img)
                    
                embed.set_author(
                        name= live_data['user_name'],
                        url= live_url,
                        icon_url= sub_channel['icon_url']
                        )
                embed.add_field(name= '分類', value= live_data['game_name'], inline= False)
                
                
                tag= f'<@&{sub_channel["role"]}>' if sub_channel['role'] is not None else ''
                
                ch= self.bot.get_channel(sub_channel['channel'])
                await ch.send(tag, embed= embed)
                
                print(f"\033[0;35m{datetime.now().strftime('%H:%M:%S')}\033[0m - \033[0;32m{live_data['user_name']}\033[0m 開台了")
        return self.json_data
        
    @on_live.before_loop
    async def on_live_is_ready(self):
        await self.bot.wait_until_ready()
        print('     \033[1;32m-\033[0m 開始 直播偵測')
    
async def setup(bot):
    await bot.add_cog(Task(bot))
