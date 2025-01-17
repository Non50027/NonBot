from discord.ext import commands
from discord_bot.tool import SelectFileView, CogCore
import discord, os

class Admin(CogCore):
    
    # 載入指定程式檔案
    @commands.hybrid_command()
    @commands.is_owner()
    async def load(self, ctx: commands.Context): # type: ignore
        '''載入指定檔案'''
        view= SelectFileView(function_name= self.bot.load_extension)
        await ctx.send("請選擇要載入的檔案：", view=view, ephemeral= True)

    # 卸載指令檔案
    @commands.hybrid_command()
    @commands.is_owner()
    async def unload(self, ctx: commands.Context): # type: ignore
        '''卸載指定檔案'''
        view= SelectFileView(function_name= self.bot.unload_extension)
        await ctx.send("請選擇要載入的檔案：", view=view, ephemeral= True)

    # 重新載入程式檔案
    @commands.hybrid_command()
    @commands.is_owner()
    async def reload(self, ctx: commands.Context): # type: ignore
        '''重新載入指定檔案'''
        view= SelectFileView(function_name= self.bot.reload_extension)
        await ctx.send("請選擇要載入的檔案：", view=view, ephemeral= True)
        

async def setup(bot):
    await bot.add_cog(Admin(bot))
