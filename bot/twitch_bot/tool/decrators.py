import os
from functools import wraps
from twitchio.ext import commands

class MyDecorators():
    
    @staticmethod
    def select_channel(function_name):
        '''
        限制命令頻道
        '''
        # 繼承方法原來的狀態
        @wraps(function_name)
        async def inner(self, ctx: commands.Context, *args, **kwargs):
            
            # if ctx.channel.name in ['infinite0527', 'samoago']:
            if ctx.channel.name in ['infinite0527', 'hennie2001', 'samoago', 'mikiaoboshi']:
                await function_name(self, ctx, *args, **kwargs)
            else:
                print(f' {ctx.author.display_name} 嘗試在 {ctx.channel.name} 使用指令')
        return inner
    
    @staticmethod
    def api_headers(function_name):
        '''
        連接API時使用的 headers settings
        並存在 self.headers
        '''
        @wraps(function_name)
        async def inner(self, ctx: commands.Context, *args, **kwargs):
            headers = {
                'Client-ID': os.getenv('VITE_TWITCH_BOT_ID'),
                'Authorization': f"Bearer {os.getenv('TWITCH_BOT_TOKEN')}"
            }
            self.headers= headers
            await function_name(self, ctx, *args, **kwargs)
        
        return inner
