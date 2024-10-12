import discord, asyncio, os
from discord.ext import commands
from .serve import get_file_dir_list

class Bot(commands.Bot):
    def __init__(self) :
        super().__init__(
            command_prefix= "!",
            intents= discord.Intents.all(),
            help_command= None
        )
        print(f'\n\033[0;36mDiscord Bot\033[0m 啟動中 ...')
    
    async def load_extensions(self):
        file_list= get_file_dir_list(os.path.dirname(os.path.dirname(__file__)))
        for file in file_list:
            try:
                _= file.split('\\')
                print(f'    \033[1;32m - \033[0m{_[-1][:-3]} ... ', end='')
                _= file.split('discord_bot\\')[-1].split('\\')
                await self.load_extension('.'.join(_)[:-3])
                print('\033[1;32mOK\033[0m')
            except Exception as e:
                print(f'失敗 : \033[0;31m{e}\033[0m')

    # 會在機器人登入後但在連接到 Websocket 之前執行
    async def setup_hook(self) -> None:
        '''
        會在機器人登入後但在連接到 Websocket 之前執行
        ''' 
        
        print(f'   \033[1;32m-\033[0m 已登入帳號 | \033[0;32m{self.user}\033[0m')
        
        # 載入檔案
        print('   \033[1;32m-\033[0m 載入檔案 ... ')
        self.loop.create_task(self.load_extensions())
        
        # 查看載入成功的 / 指令
        print(f'   \033[1;32m-\033[0m 載入指令：\033[1;35m{len(await asyncio.create_task(self.tree.sync()))}\033[0m 條')

    async def get_cog_commands(self):
        self.get_cog