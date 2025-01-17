from discord.ext import commands
import aiohttp

class CogCore(commands.Cog):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot= bot
    
    async def get_ctx(self):
        ch= self.bot.get_channel(656791892440121354)
        msg= await ch.fetch_message(1289805561952600126)
        ctx= await self.bot.get_context(msg)
        return ctx

    async def post_data(self, url, data= None):
        async with aiohttp.ClientSession() as session:
            header= {
                'accept': 'application/json'
            }
            async with session.post(url, headers=header, data= data) as response:
                response_data= await response.json()
                if response.status== 200:
                    return response_data
                elif response.status== 403: 
                    print("資料已經存在，無法新增！")
                    return None
                else:
                    print(f"發生錯誤，狀態碼: {response.status}")
                    print(response.text)

    async def get_data(self, url):
        async with aiohttp.ClientSession() as session:
            header= {
                'accept': 'application/json'
            }
            async with session.get(url, headers=header) as response:
                response_data= await response.json()
                if response.status== 200:
                    return response_data
                else:
                    print(f"發生錯誤，狀態碼: {response.status}")
                    print(response.text)