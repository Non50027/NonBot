import os
from twitchio.ext import commands


class Bot(commands.Bot) :
    def __init__(self, token: str, secret: str):
        super().__init__(
            prefix='!',
            token= token,
            client_secret= secret
        )
        
    
    def _cog(self, fun_name):
        for filename in os.listdir(os.path.dirname(__file__)):
            if filename.startswith('_') or not filename.endswith('.py'): continue
                
            try:
                print(f'    \033[1;32m-\033[0m {filename[:-3]} ... ', end='')
                module_name = f'bot_twitch.{filename[:-3]}'
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
    