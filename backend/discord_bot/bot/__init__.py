import discord, asyncio, json
from discord.ext import commands
from . import events, cmds
from functools import wraps


class Bot(commands.Bot):
    def __init__(self) :
        super().__init__(
            command_prefix= "|",
            intents= discord.Intents.all(),
            help_command= None
        )
        print(f'\nDiscord Bot 啟動中...\n')
    
    # 會在機器人登入後但在連接到 Websocket 之前執行
    async def setup_hook(self) -> None:
        '''
        會在機器人登入後但在連接到 Websocket 之前執行
        ''' 
        
        print(f'\nDiscord Bot - 已登入帳號 ...  {self.user}')
        
        # 載入檔案
        print('Discord Bot - 載入檔案 ... ', end= '')
        events.load(self)
        cmds.load(self)
        print('OK')     
        
        # 查看載入成功的 / 指令
        print(f'Discord Bot - 載入指令：{len(await asyncio.create_task(self.tree.sync()))} 條')
        print('Discord Bot - 啟動完成\n')
        

class CogCore(commands.Cog):
    def __init__(self, bot: commands.Bot) :
        super().__init__(bot)
        
    @staticmethod
    def readJson(jsonFileName: str):
        '''
        讀取資料作為參數傳給裝飾的方法使用
        並將加工後的資料存回去
        
        讀取data中json檔
        jsonFileName (str): 檔案名稱
        '''
        def inner(functionName):
            
            # 繼承方法原來的狀態
            @wraps(functionName)
            async def wrapper(self, *args, **kwargs):
                
                # read json
                with open(f'{jsonFileName}.json', 'r', encoding='utf8') as file:
                    data= json.load(file)
                
                '''
                hybrid_command方法無法直接接收 dict 參數
                也不接收寫入kwargs
                也由於需要裝飾的方法有可能會擁有像是 ctx 這種限定位置的引數
                所以直接加入到 self中
                也應為這樣只能裝飾
                '''
                self.data= data
                result = await functionName(self, *args, **kwargs)
                
                # save json
                with open(f'{jsonFileName}.json', 'w', encoding='utf8') as file:
                    json.dump(result, file, ensure_ascii=False, indent=4)
                    
            return wrapper
        return inner