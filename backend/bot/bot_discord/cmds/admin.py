from discord.ext import commands
from bot_discord.tool import SelectFileView, CogCore, MyDecorators
import discord, os

class Admin(CogCore):
    
    # 載入指定程式檔案
    @commands.hybrid_command()
    @commands.is_owner()
    async def load(self, ctx: commands.Context): # type: ignore
        '''載入指定檔案'''
        view= SelectFileView(function_name= self.bot.load_extension)
        await ctx.send("請選擇要載入的檔案：", view=view, ephemeral= True, delete_after= 27.5)

    # 卸載指令檔案
    @commands.hybrid_command()
    @commands.is_owner()
    async def unload(self, ctx: commands.Context): # type: ignore
        '''卸載指定檔案'''
        view= SelectFileView(function_name= self.bot.unload_extension)
        await ctx.send("請選擇要載入的檔案：", view=view, ephemeral= True, delete_after= 27.5)

    # 重新載入程式檔案
    @commands.hybrid_command()
    @commands.is_owner()
    async def reload(self, ctx: commands.Context): # type: ignore
        '''重新載入指定檔案'''
        view= SelectFileView(function_name= self.bot.reload_extension)
        await ctx.send("請選擇要載入的檔案：", view=view, ephemeral= True, delete_after= 27.5)
        
    
    @commands.hybrid_command()
    @commands.is_owner()
    @MyDecorators.readJson('test')
    async def upload_psw(self, ctx: commands.Context, t: str): # type: ignore
        
        hash_psw= self.hash_password(t)
        
        self.json_data.update({
            ctx.author.name: hash_psw
        })
        return self.json_data
    
    @commands.hybrid_command()
    @commands.is_owner()
    @MyDecorators.readJson('test')
    async def q_psw(self, ctx: commands.Context, t: str): # type: ignore
        
        if ctx.author.name not in self.json_data:
            print('json key is error' , self.json_data)
        print(self.json_data)
        hash_psw= self.json_data[ctx.author.name]
        
        if self.verify_password(t, hash_psw):
            print('OK')
        else:
            print("password is error")
        

async def setup(bot):
    await bot.add_cog(Admin(bot))
