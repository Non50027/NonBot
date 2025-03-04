import twitchio, random, time, asyncio, requests, os
from datetime import datetime
from twitchio.ext import commands
from bot_twitch.tool import CogCore

class Message(CogCore):
    def __init__(self, bot, *args, **kwargs):
        super().__init__(bot, *args, **kwargs)
        self.cooldowns= {}        
    
    
    # 確認 CD
    def check_cooldowns(self, user_name: str, cd: int) -> bool:
        '''
        user_name (str): 項目名
        cd (int): CD 秒數
        True is not CD
        False is CD
        '''
        current_time= time.time()
        last_used = self.cooldowns.get(user_name, 0)  # 取得用戶上次使用時間...默認 0

        # CD 中
        if current_time - last_used < cd: return True
        
        self.cooldowns[user_name] = current_time
        return False
    
    # 偵測聊天室訊息
    @commands.Cog.event()
    async def event_message(self, message: twitchio.Message):
        # 檢查 message.author 是否為 None
        # 這是由於我的BOT名稱跟我的名稱一樣引起的
        if message.author is None: return
        # 檢查訊息內容是否包含自訂指令
        ctx = await self.bot.get_context(message)
        # 如果是指令
        if ctx.command:
            if message.channel.name!= 'pigeoncwc': return
            await self.bot.handle_commands(message)
            return
        
        # 排除自己 & bot
        if any(message.author.name== name for name in [self.bot.nick, 'nightbot', 'streamelements', 'moobot']): return
        
        try:
            await self.message_response(message)
            await self.repeat_message(message)
        except Exception as e:
            self.flag= False
            print('auto message error', e)
    
            
def prepare(bot):
    bot.add_cog(Message(bot))
