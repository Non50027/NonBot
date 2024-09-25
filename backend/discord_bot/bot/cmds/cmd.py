import tracemalloc, datetime, time, os, requests#, django
from discord.ext import commands
# from serializers import CreateRankChat

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.backend.settings')
# django.setup()

# from rest_framework.exceptions import ValidationError

class Cmd(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot= bot
        super().__init__()
    
    @commands.hybrid_command(aliases=[""])
    async def test(self, ctx: commands.Context):
        data= {
            'guild': ctx.guild.id,
            'member': ctx.author.id,
            'type': 'chat',
            'day':[__.id for __ in _.emojis],
            'value':[__.id for __ in _.roles]
        } 
        # serializer= CreateRankChat(data)
        # if serializer.is_valid():
        #     guild= serializer.save()
        #     print(guild)
        # else:
        #     raise ValidationError(serializer.errors)
        
    
    @commands.hybrid_command()
    async def ck_twitch_token(self, ctx:commands.Context):
        url= 'https://id.twitch.tv/oauth2/validate'
        
        headers = {
        'Authorization': f"Bearer {os.getenv('TWITCH_BOT_TOKEN')}"
        }   
        response= requests.get(url, headers= headers)
        data= response.json()
        msg= ''
        if response.status_code==200:
            msg= f"twitch token OK\n登入帳號：{data['login']}\n權限範圍：{', '.join(data['scopes'])}\n剩餘時間：{data['expires_in']}"
        else:
            msg= f"twitch token 失效 {data['status']}, {data['message']}"
        await ctx.send(msg)
    
    # return bot ping
    @commands.hybrid_command(description= '可以查看延遲', aliases= ['延遲'])
    @commands.is_owner()
    async def ping(self, ctx: commands.Context):
        '''
        可以查看延遲
        目前的時間
        '''
        await ctx.send(
f'''Bot延遲時間: {self.bot.latency*1000:.3f}(ms)
現在時間:
\t{datetime.datetime.now()}
\t{time.time()}''', ephemeral= True)
    
    @commands.hybrid_command(aliases=["cmd", "查看記憶體使用"])
    async def cmd_memory(self, ctx: commands.Context):
        '''
        前10個 記憶體分配最多的程式碼位置及數量大小
        '''
        # 運行中獲取記憶體分配資訊
        snapshot = tracemalloc.take_snapshot()
        top_stats = snapshot.statistics('lineno')
        top_stats= '\n'.join(['\n'.join([str(_.traceback), f'\tsize: {_.size/1024:.3f} MiB', f'\tcount: {_.count} ']) for _ in top_stats[:10]])
        
        await ctx.send(f'前10個記憶體分配最多的程式碼位置:\n{top_stats}', ephemeral= True) 
    
# Cog 載入 Bot 中
async def setup(bot):
    await bot.add_cog(Cmd(bot))