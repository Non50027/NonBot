import discord
from discord.ext import commands
from bot.tool import CogCore

class Error(CogCore):

    @commands.Cog.listener()        
    async def on_command_error(self, ctx, error):
        
        print(error)
        
        # 錯誤訊息 (用海苔遮起來)
        await ctx.send('||'+ str(error)+ '||', ephemeral= True)
        
        # 排除客製化例外處理
        if hasattr(ctx.command, 'on_error'):
            return
        
        # 缺少必要參數
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send('巧婦難為無米之炊', ephemeral= True)
        
        # 參數解析錯誤
        elif isinstance(error, commands.ArgumentParsingError):
            await ctx.send('這參數我看不懂...', ephemeral= True)
        
        # 指令未定義
        elif isinstance(error, commands.CommandNotFound):
            await ctx.send('我書讀得少...看不懂你在打什麼\n你要不要用 |help 看看我會什麼', ephemeral= True)
        
        # 應該是缺少必要的協程?
        elif 'coroutine' in str(error).split(' '):
            await ctx.send('缺少必要的協程', ephemeral= True)
        
        # 對象並未定義 send()
        elif isinstance(error, AttributeError):
            await ctx.send('我在好像在跟空氣說話', ephemeral= True)
        
        # 找不到.ch
        elif isinstance(error, commands.ChannelNotFound):
            await ctx.send('迷路了...頻道到底在哪QQ', ephemeral= True)
        
        # 其他例外
        else:
            await ctx.send('我不會 இдஇ', ephemeral= True)

async def setup(bot):
    await bot.add_cog(Error(bot))