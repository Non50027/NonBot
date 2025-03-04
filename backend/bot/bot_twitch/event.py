import twitchio, time, os, dotenv, httpx
from datetime import datetime
from twitchio.ext import commands
from bot_twitch.tool import CogCore

class Event(CogCore):
    
    @commands.Cog.event()
    async def event_command_error(self, ctx: commands.Context, error):
        '''
        指令執行發生錯誤
        '''
        # 沒有指令
        if isinstance(error, commands.errors.CommandNotFound):
            # print(f"No --- command: {error}")
            pass
        elif isinstance(error, commands.CheckFailure):
            print('不允許的頻道', end='\r')
        # CD 中
        elif isinstance(error, commands.CommandOnCooldown):
            print(f'在 \033[0;34m{ctx.channel.name} \033[0m使用指令 \033[0;36m{ctx.command.name}\033[0m CD 中 ... 剩下 \033[0;32m{error.retry_after:.2f}\033[0m 秒')
        else:
            print(f'指令執行發生錯誤：{error}')
    
        
    @commands.Cog.event()
    async def event_token_expired(self):
        '''
        金鑰過期
        '''
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
        
    @commands.Cog.event()
    async def event_notice(self, message: str, msg_id: str| None, channel: twitchio.Channel| None):        
        '''
        聊天室衝突訊息
        '''
        if 'messages too quickly' in message: return
        print(f"\033[0;35m{datetime.now().strftime('%H:%M:%S')}\033[0m Notice =======\n  message: {message}")
        if msg_id: print(f"  msg_id: {msg_id}")
        if channel: print(f"  channel: {channel.name}")
    
    async def event_reconnect(self):
        '''
        IRC 斷開連結
        '''
        print(f"IRC 斷開連結...", end="\r")
        await self.connect()
            
def prepare(bot):
    bot.add_cog(Event(bot))
