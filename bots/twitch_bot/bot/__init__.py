import os, importlib#, dotenv
from twitchio.ext import commands
from functools import wraps


class Bot(commands.Bot) :
    def __init__(self, token: str, id: str):
        super().__init__(
            prefix='!',
            nick= "infinite0527",
            initial_channels= ["infinite0527", "hennie2001", "test40228", "samoago", 'reirei_neon', 'kirali_neon', 'yuzumi_neon', 'earendelxdfp', 'kspksp', 'iitifox', 'migi_tw', 'mikiaoboshi', 'hantears', 'hipudding1223'],
            token= token,
            client_id= id
        )
        print('\n\033[0;36mTwitch Bot\033[0m - 啟動中 ...')
        
        
    def load_cog(self):
        # 載入所有 cmds 底下的檔案
        for filename in os.listdir(os.path.dirname(__file__)):
            if not filename.startswith('_') and filename.endswith('.py'):
                try:
                    print(f'     \033[1;32m-\033[0m {filename[:-3]} ... ', end='')
                    module_name = f'bot.{filename[:-3]}'
                    module = importlib.import_module(module_name)
                    module.setup(self)
                    print('\033[1;32mOK\033[0m')
                except Exception as e:
                    print(f'失敗 : \033[0;31m{e}\033[0m')
                    
    async def event_ready(self):
        
        print(f'   \033[1;32m-\033[0m 已登入帳號 | \033[0;32m{self.nick}\033[0m')
        print('   \033[1;32m-\033[0m 載入檔案 ...')
        
        self.load_cog()
        
        print(f'   \033[1;32m-\033[0m 載入指令: \033[1;35m{len(self.commands)}\033[0m 條')
        print('  \033[1;32m-\033[0;36m 啟動完成\033[0m')
    
    # 複寫原方法
    async def event_command_error(self, ctx: commands.Context, error):
        
        # 沒有指令
        if isinstance(error, commands.errors.CommandNotFound):
            # print(f"No command: {error}")
            pass
        
        # CD 中
        elif isinstance(error, commands.CommandOnCooldown):
            print(f'指令 CD 中 ... 剩下 {error.retry_after:.2f} 秒')
        else:
            print(f'指令執行發生錯誤：{error}')

class CogCore(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot= bot
        # load .env file
        # dotenv.load_dotenv()
        self.token= os.getenv('TWITCH_BOT_TOKEN'),
        self.id= os.getenv('VITE_TWITCH_BOT_ID')
    
    @staticmethod
    def select_channel(function_name):
        '''
        限制命令頻道
        '''
        # 繼承方法原來的狀態
        @wraps(function_name)
        async def inner(self, ctx: commands.Context, *args, **kwargs):
            
            # if ctx.channel.name in ['infinite0527', 'samoago']:
            if ctx.channel.name in ['infinite0527', 'hennie2001', 'samoago', 'mikiaoboshi']:
                await function_name(self, ctx, *args, **kwargs)
            else:
                print(f' {ctx.author.display_name} 嘗試在 {ctx.channel.name} 使用指令')
        return inner
    
    @staticmethod
    def api_headers(function_name):
        '''
        連接API時使用的 headers settings
        並存在 self.headers
        '''
        @wraps(function_name)
        async def inner(self, ctx: commands.Context, *args, **kwargs):
            headers = {
                'Client-ID': self.id,
                'Authorization': f'Bearer {self.token[0]}'
            }
            self.headers= headers
            await function_name(self, ctx, *args, **kwargs)
        
        return inner
