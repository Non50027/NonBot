import tracemalloc, os, requests, discord, time
from discord.ext import commands
from bot.tool import CogCore

class Cmd(CogCore):
    
    @commands.hybrid_command()
    async def test(self, ctx: commands.Context):
        cog= self.bot.get_cog('Live')
        ch= self.bot.get_channel(656791892440121354)
        msg= await ch.fetch_message(1289805561952600126)
        ctx= await self.bot.get_context(msg)
        cmd= self.bot.get_command('meg')
        print(cmd)
        await cmd(ctx)
        # await ctx.send(os.getenv('TWITCH_BOT_TOKEN'), ephemeral= True)
        
    @commands.hybrid_command()
    async def ck_twitch_token(self, ctx:commands.Context):
        
        response = requests.get(f"{os.getenv('VITE_BACKEND_DJANGO_URL')}/oauth/check_twitch_token/", verify=False)
        response_data= response.json()
        
        if response.status_code==200:
            msg= f"twitch token OK\n登入帳號：{response_data['login']}\n權限範圍：{', '.join(response_data['scopes'])}\n剩餘時間：{time.strftime('%H: %M: %S', time.gmtime((response_data['expires_in'])))}"
        else:
            msg= f"twitch token 失效 {response_data['status']}, {response_data['message']}"
        await ctx.send(msg, ephemeral= True)
    
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
        icon= discord.File(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))) ,"data\\icon.png"), filename= 'icon.png')
        embed.set_author(name= '農農的小烏龜', icon_url= 'attachment://icon.png')
        
        await ctx.send(file= icon, embed= embed)
        
    
# Cog 載入 Bot 中
async def setup(bot):
    await bot.add_cog(Cmd(bot))