import json, requests
from bot import CogCore
from twitchio.ext import commands


class Cmd(CogCore):
    def __init__(self, *args, **kwargs):
        super().__init__( *args, **kwargs)
        self.msg= ''
    
    # 更改回復指令的回覆內容
    @commands.command()
    @commands.cooldown(rate=1, per=10, bucket=commands.Bucket.channel)
    @CogCore.selectChannel
    async def setMsg(self, ctx: commands.Context, cmdName: str, message: str):
        '''修改指令回覆內容'''
        self.msg = message
        await ctx.channel.send(f'指令設置成功...內容為: {self.msg}')
    
    # 回復指定訊息
    @commands.command()
    @commands.cooldown(rate=1, per=10, bucket=commands.Bucket.channel)
    @CogCore.selectChannel
    async def n_test(self, ctx: commands.Context):
        '''回復指定訊息'''
        print(f"在{ctx.channel.name}使用指令輸出 -> {self.msg}")
        await ctx.channel.send(self.msg)
        
    # 取得頻道基本資訊
    @commands.command(aliases= ['getChId'])
    @commands.cooldown(rate=1, per=10, bucket=commands.Bucket.channel)
    @CogCore.selectChannel
    @CogCore.connnectAPI
    async def getChannelId(self, ctx: commands.Context, channelName: str):
        '''取得頻道基本資訊'''
        url= f"https://api.twitch.tv/helix/users?login={channelName}"
        r= requests.get(url, headers=self.headers)
        data= r.json()
        print(data)
        
    # 取得頻道開台資訊
    @commands.command(aliases= ['Live'])
    @CogCore.selectChannel
    @CogCore.connnectAPI
    async def live(self, ctx: commands.Context, channelId: str):
        '''取得頻道開台資訊'''
        url= f'https://api.twitch.tv/helix/streams?user_id={channelId}'
        r= requests.get(url, headers= self.headers)
        data= r.json()
        print(data['data'])
        
def setup(bot):
    bot.add_cog(Cmd(bot))