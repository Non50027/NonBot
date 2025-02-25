import os, aiohttp, requests, dotenv
from discord.ext import commands
from discord import Object
    
async def fetch_twitch_data(url, headers):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            response_data= await response.json()
            return response_data if response_data else None
        
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


def restart_task(func):
    try:
        if func.is_running():
            func.stop()
        func.start()
    except Exception as e:
        print('live task start error', e)

def create_ctx(bot: commands.Bot)-> commands.Context:
    class MockMessage:
        def __init__(self, bot):
            self._state = bot._connection
            self.channel = Object(id=656791892440121354)
            self.author = Object(id=123456789)  # 假設的作者 ID
            self.guild = None
    mock_message = MockMessage(bot)
    ctx = commands.Context(
        bot= bot,
        message= mock_message,
        view= None
    )
    return ctx