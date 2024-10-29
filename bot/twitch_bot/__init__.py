import os, importlib, gc, requests, dotenv, time, httpx
from twitchio.ext import commands as twitch_commands
from discord.ext import commands as discord_commands
from datetime import datetime


class Bot(twitch_commands.Bot) :
    def __init__(self, token: str, discord_bot: discord_commands.Bot= None):
        super().__init__(
            prefix='!',
            token= token,
        )
        self.discord: discord_commands.Bot= discord_bot
        self.twitch= self
        print('\n\033[0;36mTwitch Bot\033[0m - 啟動中 ...')
        
    def load_cog(self):
        # 載入所有 cmd 底下的檔案
        for filename in os.listdir(os.path.dirname(__file__)):
            if not filename.startswith('_') and filename.endswith('.py'):
                try:
                    print(f'     \033[1;32m-\033[0m {filename[:-3]} ... ', end='')
                    module_name = f'twitch_bot.{filename[:-3]}'
                    self.load_module(module_name)
                    print('\033[1;32mOK\033[0m')
                except Exception as e:
                    print(f'失敗 : \033[0;31m{e}\033[0m')
                    
    async def event_ready(self):
        
        print(f'   \033[1;32m-\033[0m 已登入帳號 | \033[0;32m{self.nick}\033[0m')
        print('   \033[1;32m-\033[0m 載入檔案 ...')
        
        self.load_cog()
        
        print(f'   \033[1;32m-\033[0m 載入指令: \033[1;35m{len(self.commands)}\033[0m 條')
        print('  \033[1;32m-\033[0;36m 啟動完成\033[0m')


    # 指令執行後觸發...無論指令是否失敗
    async def global_after_invoke(self, ctx: twitch_commands.Context):
        """
        指令執行後觸發...無論指令是否失敗
        """
        print(f"\033[0;35m{datetime.now().strftime('%H:%M:%S')}\033[0m - 指令 {ctx.command.name} 在 {ctx.channel.name} 被 {ctx.author.name} 執行")
        
        # 強制執行垃圾回收
        gc.collect()
        
    
    # 複寫原方法
    async def event_command_error(self, ctx: twitch_commands.Context, error):
        
        # 沒有指令
        if isinstance(error, twitch_commands.errors.CommandNotFound):
            # print(f"No --- command: {error}")
            pass
        
        # CD 中
        elif isinstance(error, twitch_commands.CommandOnCooldown):
            print(f'指令 CD 中 ... 剩下 {error.retry_after:.2f} 秒')
        else:
            print(f'指令執行發生錯誤：{error}')
    
    
    async def event_reconnect(self):
        self.token= os.getenv('TWITCH_BOT_TOKEN')
        print(f"重新連接 ... | {self.nick}")
        
        
    async def event_token_expired(self):
        
        print("Twitch token 已過期，正在嘗試更新...(；´д｀)")
        # async with httpx.AsyncClient() as client:
        #     response = await client.get(f"{os.getenv('VITE_BACKEND_DISCORD_URL')}/oauth/refresh-twitch-token")
        
        response = requests.get(f"{os.getenv('VITE_BACKEND_DJANGO_URL')}/oauth/re_get_twitch_token/")
        response_data= response.json()
        
        if response.status_code==200:
            del os.environ['TWITCH_BOT_TOKEN']
            del os.environ['TWITCH_BOT_REFRESH_TOKEN']
            dotenv.load_dotenv()
            
            print(f"Twitch Token 刷新成功 ヾ(＾∇＾) ... ")
            print(f"新的時間為: \033[0;35m{time.strftime('%H: %M: %S', time.localtime( time.time()+ response_data['expires_in']))}\033[0m")
            return response_data['access_token']
        else:
            print(f"刷新 Twitch Token 失敗 (T_T) : {response}")
            return None
        