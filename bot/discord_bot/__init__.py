import discord, asyncio, os, dotenv
from discord.ext import commands
from twitchio.ext import commands as twitch_commands

dotenv.load_dotenv()

class Bot(commands.Bot):
    def __init__(self) :
        super().__init__(
            command_prefix= "!",
            intents= discord.Intents.all(),
            help_command= None
        )
    
    async def load_extensions(self):
        # 將樹狀目錄下的檔案包含路徑輸出為 List
        def get_file_dir_list(dir_path: str)-> list[str]:
            ''''
            將樹狀目錄下的檔案包含路徑輸出為 List
            dir_path (str): 根目錄
            '''
            file_dir_list= []
            for root, dirs, files in os.walk(dir_path):
                if root.endswith('tool') or root.endswith('server'): continue
                    
                for file in files :
                    
                    if not file.endswith('.py'): continue
                    if file[0]=='_' or file.startswith('api_'): continue
                    if file=='bot.py': continue
                        
                    file_dir_list.append(os.path.join(root, file))
                    
            return file_dir_list
        
        file_list= get_file_dir_list(os.path.dirname(__file__))
        for file in file_list:
            try:
                _= file.split('\\')
                if _[-1].startswith('_'): 
                    print(f'    \033[1;32m - \033[0m{_[-1][:-3]} ... 未完成的檔案', end='')
                    continue
                print(f'    \033[1;32m - \033[0m{_[-1][:-3]} ... ', end='')
                _= ['discord_bot']+file.split('discord_bot\\')[-1].split('\\')
                await self.load_extension('.'.join(_)[:-3])
                print('\033[1;32mOK\033[0m')
            except Exception as e:
                print(f'失敗 : \033[0;31m{e}\033[0m')

    # 會在機器人登入後但在連接到 Websocket 之前執行
    async def setup_hook(self) -> None:
        '''
        會在機器人登入後但在連接到 Websocket 之前執行
        ''' 
        print(f'\n\n\033[0;36mDiscord Bot\033[0m 啟動中 ...')
        print(f'   \033[1;32m-\033[0m 已登入帳號 | \033[0;32m{self.user}\033[0m')
        
        # 載入檔案
        print('   \033[1;32m-\033[0m 載入檔案 ... ')
        self.loop.create_task(self.load_extensions())
        
        # 查看載入成功的 / 指令
        print(f'   \033[1;32m-\033[0m 載入指令：\033[1;35m{len(await asyncio.create_task(self.tree.sync()))}\033[0m 條')
    
bot= Bot()

async def start_bot():
    await bot.start(os.getenv('DISCORD_BOT_TOKEN'))
    
# async def get_bot():
#     return bot