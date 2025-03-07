import tracemalloc, os, discord, orjson
from discord.ext import commands
from bot_discord.tool import CogCore
from bot_discord.tool import MyDecorators

class Cmd(CogCore):
        
    @commands.hybrid_command()
    @commands.is_owner()
    async def test(self, ctx: commands.Context):
        view= discord.ui.View()
        button= discord.ui.Button(
            label= "VOD",
            url= 'https://www.youtube.com/watch?v=yUBxaveNEPs'
        )
        view.add_item(button)
        await ctx.send(view= view)
    
    # return bot ping
    @commands.hybrid_command(description= '可以查看延遲', aliases= ['延遲'])
    @commands.is_owner()
    async def ping(self, ctx: commands.Context):
        '''可以查看延遲'''
        await ctx.send(f"Bot延遲時間: {self.bot.latency*1000:.3f}(ms)", ephemeral= True)
    
    @commands.hybrid_command(aliases=["cmd", "查看記憶體使用"])
    async def cmd_memory(self, ctx: commands.Context):
        '''前10個 記憶體分配最多的程式碼位置及數量大小'''
        # 運行中獲取記憶體分配資訊
        snapshot = tracemalloc.take_snapshot()
        top_stats = snapshot.statistics('lineno')
        top_stats= '\n'.join(['\n'.join([str(_.traceback), f'\tsize: {_.size/1024:.3f} MiB', f'\tcount: {_.count} ']) for _ in top_stats[:10]])
        
        await ctx.send(f'前10個記憶體分配最多的程式碼位置:\n{top_stats}', ephemeral= True) 
    
        # 同步 / 指令
    @commands.hybrid_command(name= "sync", description= "同步 / 指令",)
    @commands.is_owner()
    async def sync(self, ctx: commands.Context):
        
        ctx.bot.tree.copy_global_to(guild=ctx.guild)
        _= await ctx.bot.tree.sync(guild=ctx.guild)
        
        embed= discord.Embed(
            description= f"已同步 / 指令 {len(_)} 條",
            color= 0xABFFE4
        )
        icon= discord.File(os.path.join(os.path.dirname(os.path.dirname(__file__)) ,"data\\icon.png"), filename= 'icon.png')
        embed.set_author(name= '農農的小烏龜', icon_url= 'attachment://icon.png')
        
        await ctx.send(file= icon, embed= embed)
    
    @commands.hybrid_command()
    @MyDecorators.readJson('test')
    async def  test(self, ctx:commands.Context, cmd: str, *, context: str):
        
        if not cmd.startswith('!'):
            await ctx.send("請以`!`開頭")
            return
         
        cmds= self.json_data.setdefault(ctx.channel.name, {})
        cmds[cmd]= context
            
        return self.json_data
    
# Cog 載入 Bot 中
async def setup(bot):
    await bot.add_cog(Cmd(bot))