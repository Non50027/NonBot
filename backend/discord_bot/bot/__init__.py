import discord, asyncio, json
from discord.ext import commands
from . import events, cmds


class Bot(commands.Bot):
    def __init__(self) :
        super().__init__(
            command_prefix= "|",
            intents= discord.Intents.all(),
            help_command= None
        )
        print(f'\n\033[0;36mDiscord Bot\033[0m 啟動中...')
    
    # 會在機器人登入後但在連接到 Websocket 之前執行
    async def setup_hook(self) -> None:
        '''
        會在機器人登入後但在連接到 Websocket 之前執行
        ''' 
        
        print(f'   \033[1;32m-\033[0m 已登入帳號 | \033[0;32m{self.user}\033[0m')
        
        # 載入檔案
        print('   \033[1;32m-\033[0m 載入檔案 ... ', end= '')
        events.load(self)
        cmds.load(self)
        print('\033[0;32mOK\033[0m')
        
        # 查看載入成功的 / 指令
        print(f'   \033[1;32m-\033[0m 載入指令：\033[1;35m{len(await asyncio.create_task(self.tree.sync()))}\033[0m 條')
        