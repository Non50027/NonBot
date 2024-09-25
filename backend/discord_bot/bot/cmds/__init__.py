import discord, asyncio, os
from discord.ext import commands
from discord import app_commands
from enum import Enum

def load(bot):
    
    # print('src', os.path.dirname(__file__).replace('\\', '.')[3:]+'.')
    # 載入所有 同目錄 底下的檔案 非 _開頭.py
    asyncio.gather(*[bot.load_extension('bot.cmds.'+_[:-3]) for _ in os.listdir(os.path.realpath(os.path.dirname(__file__))) if not _.startswith('_') and _.endswith('.py')])
    
    FileList= Enum('FileList', {_[:-3]: _[:-3] for _ in os.listdir(os.path.realpath(os.path.dirname(__file__))) if not _.startswith('_') and _.endswith('.py')})
    
    src= 'bot.cmds.'

    # 載入指定程式檔案
    @bot.hybrid_command()
    @commands.is_owner()
    @app_commands.describe(filename= '檔案名稱')
    # @app_commands.choices(filename= choices)
    async def load(ctx: commands.Context, filename: FileList): # type: ignore
        '''
        + 檔名(不需要.py): 載入指定檔案
        '''
        await bot.load_extension(src+ filename.name)
        await ctx.send(f"載入 {filename.name} ...OK", ephemeral= True)

    # 卸載指令檔案
    @bot.hybrid_command()
    @commands.is_owner()
    # @app_commands.choices(filename= choices)
    @app_commands.describe(filename= '檔案名稱')
    async def unload(ctx: commands.Context, filename: FileList): # type: ignore
        '''
        + 檔名(不需要.py): 卸載指定檔案    
        '''
        await bot.unload_extension(src+filename.name)
        await ctx.send(f"卸載 {filename.name} ...OK", ephemeral= True)

    # 重新載入程式檔案
    @bot.hybrid_command()
    @commands.is_owner()
    # @app_commands.choices(filename= choices)
    @app_commands.describe(filename= '檔案名稱')
    async def reload(ctx: commands.Context, filename: FileList): # type: ignore
        '''
        + 檔名(不需要.py): 重新載入指定檔案
        '''
        await bot.reload_extension(src+filename.name)
        await ctx.send(f"重載 {filename.name} ...OK", ephemeral= True)
    
    # 同步 / 指令
    @bot.hybrid_command(name= "sync", description= "同步 / 指令",)
    @commands.is_owner()
    async def sync(ctx: commands.Context):
        
        ctx.bot.tree.copy_global_to(guild=ctx.guild)
        _= await ctx.bot.tree.sync(guild=ctx.guild)
        
        print(f"已在 {ctx.message.guild.name} 同步 / 指令 {len(_)} 條")
        # await ctx.send(f"已同步 / 指令 {len(_)} 條")
        
        embed= discord.Embed(
            description= f"已同步 / 指令 {len(_)} 條",
            color= 0xABFFE4
        )
        icon= discord.File(os.path.join(os.path.dirname(os.path.dirname(__file__)) ,"data\\icon.png"), filename= 'icon.png')
        embed.set_author(name= '農農的小烏龜', icon_url= 'attachment://icon.png')
        
        await ctx.send(file= icon, embed= embed, ephemeral= True)
        
