from twitchio.ext.commands.bot import Bot
from twitch_bot.tool import CogCore
import requests, os, dotenv, tim
from discord.ext import tasks

class RefreshToken(CogCore):
    def __init__(self, bot: Bot):
        super().__init__(bot)
        self.token_time= self.get_twitch_token_time()
        self.loop_refresh_token.start()
    
    def get_twitch_token_time(self):
        response = requests.get(
            f"{os.getenv('VITE_BACKEND_DJANGO_URL')}/oauth/check_twitch_token/", 
            verify=False
            )
        response_data= response.json()
        
        return response_data['expires_in'] \
            if response.status_code==200 \
            else 1000
    
    @tasks.loop(minutes=5)
    async def loop_refresh_token(self):
        '''檢查 token 並重新獲取'''
        self.token_time -= 300  # 每次檢查後剩餘時間減少60秒（1分鐘）
        
        # 如果剩餘時間小於5分鐘，則刷新Token
        if self.token_time <= 300:  # 300秒 = 5分鐘
            try:
                print(f"刷新 Twitch Token ... ")
                response = requests.get(
                    f"{os.getenv('VITE_BACKEND_DJANGO_URL')}/oauth/re_get_twitch_token/", 
                    verify=False
                    )
                response_data= response.json()
                if response.status_code == 200:
                    del os.environ['TWITCH_BOT_TOKEN']
                    del os.environ['TWITCH_BOT_REFRESH_TOKEN']
                    dotenv.load_dotenv()
                    self.token_time = response_data['expires_in']  # 更新新的有效期
                    print(f"Twitch Token 刷新成功 ... 有效期限至: {time.strftime('%H: %M: %S', time.localtime( time.time()+ self.token_time))}")
                else:
                    print(f"刷新 Twitch Token 失敗: {response}")
            except Exception as e:
                print('error', e)
    
    @loop_refresh_token.before_loop
    async def loop_refresh_token_is_ready(self):
        '''task 開始前執行'''
        await self.bot.discord.wait_until_ready()
        print('     \033[1;32m-\033[0m 開始 Twitch Bot Token 偵測')
    
    @loop_refresh_token.after_loop
    async def loop_refresh_token_is_close(self):
        '''task 結束後執行'''
        print('     \033[1;32m-\033[0m 結束 Twitch Bot Token 偵測')
    
def setup(bot):
    bot.add_cog(RefreshToken(bot))