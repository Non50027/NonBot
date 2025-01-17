from twitchio.ext import commands
import os, aiohttp

class CogCore(commands.Cog):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot= bot
        self.token= os.getenv('TWITCH_BOT_TOKEN'),
        self.id= os.getenv('VITE_TWITCH_BOT_ID')
    
    async def post_data(self, url, data):
        async with aiohttp.ClientSession() as session:
            header= {
                'accept': 'application/json',
                'Content-Type': 'application/json' 
            }
            async with session.post(url, headers=header, json= data) as response:
                response_data= await response.json()
                if response.status== 200:
                    return response_data
                elif response.status== 403: 
                    print("資料已經存在，無法新增！")
                    return None
                else:
                    print(f"發生錯誤，狀態碼: {response.status}")
                    print(response.text)

    async def get_data(self, url, data= None):
        async with aiohttp.ClientSession() as session:
            header= {
                'accept': 'application/json',
                'Content-Type': 'application/json' 
            }
            async with session.get(url, headers=header, json= data) as response:
                response_data= await response.json()
                if response.status== 200:
                    return response_data
                else:
                    print(f"發生錯誤，狀態碼: {response.status}")
                    print(response.text)
