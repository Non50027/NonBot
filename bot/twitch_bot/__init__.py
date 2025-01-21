import os, dotenv, time, httpx, twitchio
from twitchio.ext import commands
from datetime import datetime


class Bot(commands.Bot) :
    # def __init__(self, token: str, discord_bot: discord_commands.Bot= None):
    def __init__(self, token: str, secret: str):
        super().__init__(
            prefix='!',
            token= token,
            client_secret= secret,
            initial_channels= [
                    'infinite0527',
                    'hibiki_meridianproject',
                    'zuoo846095',
                    'samoago',
                    'hennie2001',
                    'reirei_neon',
                    'kirali_neon',
                    'yuzumi_neon',
                    'test40228',
                    'yoruno_moonlit',
                    'kspksp',
                    'migi_tw',
                    'moondogs_celestial',
                    'mikiaoboshi',
                    'pigeoncwc',
                    'q771110',
                ]
        )
        
    
    def _cog(self, fun_name):
        for filename in os.listdir(os.path.dirname(__file__)):
            if filename.startswith('_') or not filename.endswith('.py'): continue
                
            try:
                print(f'    \033[1;32m-\033[0m {filename[:-3]} ... ', end='')
                module_name = f'twitch_bot.{filename[:-3]}'
                fun_name(module_name)
                print('\033[1;32mOK\033[0m')
            except Exception as e:
                print(f'失敗 : \033[0;31m{e}\033[0m')
    
    def load_cog(self):
        print('  \033[1;32m-\033[0m 載入檔案 ...')
        self._cog(self.load_module)
    
    def reload_cog(self):
        print('  \033[1;32m-\033[0m 重新載入檔案 ...')
        self._cog(self.reload_module)
                    
    async def event_ready(self):
        
        print('\n\033[0;36mTwitch Bot\033[0m - 啟動中 ...')
        print(f'  \033[1;32m-\033[0m 已登入帳號 | \033[0;32m{self.nick}\033[0m')
        
        self.load_cog()
        
        _= f'  \033[1;32m-\033[0m 載入指令: \033[1;35m{len(self.commands)}\033[0m 條\n'
        _+= '  \033[1;32m-\033[0;36m 啟動完成\033[0m'
        print(_)

    # 指令執行後觸發...無論指令是否失敗
    # async def global_after_invoke(self, ctx: twitch_commands.Context):
    #     """
    #     指令執行後觸發...無論指令是否失敗
    #     """
    #     print(f"\033[0;35m{datetime.now().strftime('%H:%M:%S')}\033[0m - 指令 {ctx.command.name} 在 {ctx.channel.name} 被 {ctx.author.name} 執行")
        
    #     # 強制執行垃圾回收
    #     gc.collect()
        
    
    # 複寫原方法
    async def event_command_error(self, ctx: commands.Context, error):
        
        # 沒有指令
        if isinstance(error, commands.errors.CommandNotFound):
            # print(f"No --- command: {error}")
            pass
        elif isinstance(error, commands.CheckFailure):
            print('不允許的頻道', end='\r')
        # CD 中
        elif isinstance(error, commands.CommandOnCooldown):
            print(f'在 \033[0;34m{ctx.channel.name} \033[0m使用指令 \033[0;36m{ctx.command.name}\033[0m CD 中 ... 剩下 \033[0;32m{error.retry_after:.2f}\033[0m 秒')
        else:
            print(f'指令執行發生錯誤：{error}')
    
        
        
    async def event_token_expired(self):
        
        print(f"\033[0;35m{datetime.now().strftime('%H:%M:%S')}\033[0m - Twitch token 已過期，正在嘗試更新...(；´д｀)")
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{os.getenv('BACKEND_URL')}/oauth/refresh-twitch-token")
        
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
        
    # async def event_join(self, channel: twitchio.Channel, user: twitchio.User):
        # print(channel.name, user.display_name)
    