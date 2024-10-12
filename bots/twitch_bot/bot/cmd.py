import requests, random
from bot.tool import CogCore, MyDecorators
from twitchio.ext import commands


class Cmd(CogCore):
    def __init__(self, *args, **kwargs):
        super().__init__( *args, **kwargs)
        self.msg= ''
    
    # 更改回復指令的回覆內容
    @commands.command()
    @commands.cooldown(rate=1, per=10, bucket=commands.Bucket.channel)
    async def setMsg(self, ctx: commands.Context, cmd_name: str, *message: str):
        '''修改指令回覆內容'''
        self.msg = message
        await ctx.channel.send(f"指令設置成功...內容為: {' '.join(self.msg)}")
    
    # 回復指定訊息
    @commands.command()
    @commands.cooldown(rate=1, per=10, bucket=commands.Bucket.channel)
    async def n_test(self, ctx: commands.Context):
        '''回復指定訊息'''
        print(f"在{ctx.channel.name}使用指令輸出 -> {self.msg}")
        _= ['Love', 'Jump', 'Horn', 'Bell', 'Hi', 'Lick', 'Jump', 'Lovely', 'Move', 'Press', 'Wink']
        _= random.choices(_, k= random.randint(1, 2))
        _= _ if len(_)>1 else _*2
        msg= f" kspksp{'  kspksp'.join(_)} "
        await ctx.channel.send(msg)
        
    # 取得頻道基本資訊
    @commands.command(aliases= ['getChId'])
    @commands.cooldown(rate=1, per=10, bucket=commands.Bucket.channel)
    @MyDecorators.api_headers
    async def getChannel_id(self, ctx: commands.Context, channel_name: str):
        '''取得頻道基本資訊'''
        url= f"https://api.twitch.tv/helix/users?login={channel_name}"
        r= requests.get(url, headers=self.headers)
        data= r.json()
        print(data)
        
    # 取得頻道開台資訊
    @commands.command(aliases= ['Live'])
    @MyDecorators.api_headers
    async def live(self, ctx: commands.Context, channel_id: str):
        '''取得頻道開台資訊'''
        url= f'https://api.twitch.tv/helix/streams?user_id={channel_id}'
        r= requests.get(url, headers= self.headers)
        data= r.json()
        print(data['data'])
        
def setup(bot):
    bot.add_cog(Cmd(bot))