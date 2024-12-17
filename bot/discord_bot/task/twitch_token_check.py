from discord_bot.tool import CogCore, restart_task
from discord.ext import tasks, commands
import os, dotenv, httpx, time, datetime

    
class TwitchTokenCheck(CogCore):
    def __init__(self, bot):
        super().__init__(bot)
        self.token_time= 0
        
    async def get_twitch_token_time(self):
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{os.getenv('VITE_BACKEND_DISCORD_URL')}/oauth/validate")
        response_data= response.json()
        
        if response.status_code== 200: self.token_time= response_data['expires_in']
        else: self.token_time= 0

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.loop.create_task(self.start_task())
        
    async def start_task(self):
        # await self.get_twitch_token_time()
        restart_task(self.check_twitch_token)
    
    @tasks.loop(hours=1)
    async def check_twitch_token(self):
        '''檢查 token 並重新獲取'''
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{os.getenv('VITE_BACKEND_DISCORD_URL')}/oauth/validate")
        if response.status_code== 200: return
        
        print(f"\033[0;35m{datetime.datetime.now().strftime('%H:%M:%S')}\033[0m - 刷新 Twitch Token ... sup")
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{os.getenv('VITE_BACKEND_DISCORD_URL')}/oauth/refresh-twitch-token")
        response_data= response.json()
        
        if response.status_code == 200:
            del os.environ['TWITCH_BOT_TOKEN']
            del os.environ['TWITCH_BOT_REFRESH_TOKEN']
            dotenv.load_dotenv()
            self.token_time = response_data['expires_in']  # 更新新的有效期
            print(f"Twitch Token 刷新成功 ... ")
            print(f"有效時間至: \033[0;35m{time.strftime('%H: %M: %S', time.localtime( time.time()+ response_data['expires_in']))}\033[0m")
        
        else:
            print(f"刷新 Twitch Token 失敗: {response}")
    
    @check_twitch_token.before_loop
    async def check_twitch_token_ready(self):
        '''task 開始前執行'''
        print('     \033[1;32m-\033[0m 開始 twitch token 輔助偵測')
    
    @check_twitch_token.after_loop
    async def check_twitch_token_close(self):
        '''task 結束後執行'''
        print('     \033[1;32m-\033[0m 結束 twitch token 輔助偵測')


async def setup(bot):
    await bot.add_cog(TwitchTokenCheck(bot))