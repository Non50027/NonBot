import os, dotenv, time, httpx, twitchio, orjson
from twitchio.ext import commands
from datetime import datetime
from tool import MyDecorators


class Bot(commands.Bot) :
    # def __init__(self, token: str, discord_bot: discord_commands.Bot= None):
    def __init__(self, token: str, secret: str):
        super().__init__(
            prefix='!',
            token= token,
            client_secret= secret
        )
        
    async def event_ready(self):
        
        print('\n\033[0;36mTwitch Bot\033[0m - 啟動中 ...')
        print(f'  \033[1;32m-\033[0m 已登入帳號 | \033[0;32m{self.nick}\033[0m')
        
        self.load_cog()
        
        _= f'  \033[1;32m-\033[0m 載入指令: \033[1;35m{len(self.commands)}\033[0m 條\n'
        _+= '  \033[1;32m-\033[0;36m 啟動完成\033[0m'
        print(_)
        
        
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
        
    async def event_notice(self, message: str, msg_id: str| None, channel: twitchio.Channel| None):        
        if 'messages too quickly' in message: return
        print(f"\033[0;35m{datetime.now().strftime('%H:%M:%S')}\033[0m Notice =======\n  message: {message}")
        if msg_id: print(f"  msg_id: {msg_id}")
        if channel: print(f"  channel: {channel.name}")
    
    async def event_reconnect(self):
        print(f"IRC 斷開連結...", end="\r")
        await self.connect()
    
    
    async def event_message(self, message: twitchio.Message):

        # 排除自己 & bot
        if any(message.author.name== name for name in [self.bot.nick, 'nightbot', 'streamelements', 'moobot']): return
        
        # 處理預設的指令
        await self.bot.handle_commands(message)
        
        # 自訂指令回應
        if message.content.startswith("!"):
            file_path= os.path.join(os.path.dirname(__file__), 'data', 'custom_cmds.json')
            with open(file_path, "rb") as f:
                custom_commands = orjson.load(f.read())
            
            channel_name = message.channel.name
            content = message.content.lower()

            if content in custom_commands.get(channel_name, {}):
                await message.channel.send(custom_commands[channel_name][content])


    @commands.command()
    @MyDecorators.readJson('custom_cmds')
    async def editcmd(self, ctx: commands.Context, cmd: str, *, context: str):
        '''
        新增自訂指令
        '''
        if not cmd.startswith('!'):
            await ctx.send("請以`!`開頭")
            return
        
        cmds= self.json_data.setdefault(ctx.channel.name, {})
        cmds[cmd]= context
            
        return self.json_data