import requests, os
from twitch_bot.tool import CogCore, MyDecorators
from twitchio.ext import commands


class Cmd(CogCore):
    def __init__(self, *args, **kwargs):
        super().__init__( *args, **kwargs)
        self.is_game= {}
        self.is_who= {}
        self.dc_url: str| None= 'https://discord.gg/rZ6QcNfSKu'
    
    def check_channel(self, ctx):
        return True if any(n== ctx.message.channel.name for n in ['pigeoncwc', 'infinite0527'])  else False
    
    # 更改回復指令的回覆內容
    @commands.command(aliases= ['setgame'])
    @commands.cooldown(rate=1, per=10, bucket=commands.Bucket.channel)
    # async def setMsg(self, ctx: commands.Context, cmd_name: str, *message: str):
    async def setGame(self, ctx: commands.Context, *message: str):
        '''修改指令回覆內容'''
        if not self.check_channel(ctx): return
        # 檢查是否是 Mod 或 Broadcaster
        if not (ctx.author.is_mod or ctx.author.name == ctx.channel.name): return
        self.is_game.setdefault(ctx.channel.name, message)
        await ctx.channel.send(f"指令設置成功...內容為: {' '.join(self.is_game[ctx.channel.name])}")
    
    # 更改回復指令的回覆內容
    @commands.command(aliases= ['setwho'])
    @commands.cooldown(rate=1, per=10, bucket=commands.Bucket.channel)
    # async def setMsg(self, ctx: commands.Context, cmd_name: str, *message: str):
    async def setWho(self, ctx: commands.Context, *message: str):
        '''修改指令回覆內容'''
        if not self.check_channel(ctx): return
        if not (ctx.author.is_mod or ctx.author.name == ctx.channel.name): return
        self.is_who.setdefault(ctx.channel.name, message)
        await ctx.channel.send(f"指令設置成功...內容為: {'、'.join(self.is_who[ctx.channel.name])}")
    
    # 更改回復指令的回覆內容
    @commands.command(aliases= ['dc_url'])
    @commands.cooldown(rate=1, per=10, bucket=commands.Bucket.channel)
    # async def setMsg(self, ctx: commands.Context, cmd_name: str, *message: str):
    async def setDcUrl(self, ctx: commands.Context, url: str):
        '''修改指令回覆內容'''
        if not self.check_channel(ctx): return
        if not (ctx.author.is_mod or ctx.author.name == ctx.channel.name): return
        self.dc_url= url
        await ctx.channel.send(f"指令設置成功")
    
    @commands.command(aliases= ['DC'])
    @commands.cooldown(rate=1, per=10, bucket=commands.Bucket.channel)
    # async def setMsg(self, ctx: commands.Context, cmd_name: str, *message: str):
    async def dc(self, ctx: commands.Context):
        '''修改指令回覆內容'''
        if ctx.message.channel.name== 'q771110':
            url= 'https://discord.gg/aDeKQMck58'
            await ctx.channel.send(f"DC邊緣人請加： {url} ")
        elif self.check_channel(ctx):
            await ctx.channel.send(f"DC 底家: {self.dc_url} 記得要去領取身分組喔~")
        
    
    # 回復指定訊息
    @commands.command(aliases= ['Game', 'GAME', 'who', 'WHO'])
    @commands.cooldown(rate=1, per=10, bucket=commands.Bucket.channel)
    async def game(self, ctx: commands.Context):
        '''回復指定訊息'''
        if not self.check_channel(ctx): return
        if self.is_who.get(ctx.channel.name) is None:
            msg= f"正在玩 {' '.join(self.is_game.get(ctx.channel.name, ''))}"
        else: 
            msg= f"正在與 {'、'.join(self.is_who[ctx.channel.name])} 遊玩 {' '.join(self.is_game.get(ctx.channel.name, ''))}"
        await ctx.channel.send(msg)
    
    # 回復指定訊息
    @commands.command(aliases= ['貓咪', '卯咪', 'CAT'])
    @commands.cooldown(rate=1, per=10, bucket=commands.Bucket.channel)
    async def cat(self, ctx: commands.Context):
        '''回復指定訊息'''
        if not self.check_channel(ctx): return
        await ctx.channel.send("什麼 早安 晚安 不知道")
    
    # 回復指定訊息
    @commands.command()
    @commands.cooldown(rate=1, per=10, bucket=commands.Bucket.channel)
    async def 你失敗了(self, ctx: commands.Context):
        '''回復指定訊息'''
        if not self.check_channel(ctx): return
        await ctx.channel.send("但你仍可以繼續玩")
    
    
    # 取得頻道基本資訊
    @commands.command(aliases= ['getChId'])
    @commands.cooldown(rate=1, per=10, bucket=commands.Bucket.channel)
    @MyDecorators.api_headers
    async def getChannel_id(self, ctx: commands.Context, channel_name: str):
        '''取得頻道基本資訊'''
        if not self.check_channel(ctx): return
        url= f"https://api.twitch.tv/helix/users?login={channel_name}"
        r= requests.get(url, headers=self.headers)
        data= r.json()
        print(data)
        
    # 取得頻道開台資訊
    @commands.command(aliases= ['Live'])
    @MyDecorators.api_headers
    async def live(self, ctx: commands.Context, channel_id: str):
        '''取得頻道開台資訊'''
        if not self.check_channel(ctx): return
        url= f'https://api.twitch.tv/helix/streams?user_id={channel_id}'
        r= requests.get(url, headers= self.headers)
        data= r.json()
        print(data['data'])
        
    
    # 取得頻道基本資訊
    @commands.command()
    @commands.cooldown(rate=1, per=10, bucket=commands.Bucket.channel)
    @MyDecorators.api_headers
    async def test_getuser(self, ctx: commands.Context):
        '''取得頻道基本資訊'''
        if not self.check_channel(ctx): return
        # url= f"https://api.twitch.tv/helix/users"
        # r= requests.get(url, headers=self.headers)
        # data= r.json()
        data= await self.bot.fetch_users(token= os.getenv('TWITCH_BOT_TOKEN'))
        print(data)
        
    # 更改回復指令的回覆內容
    @commands.command(aliases= ["小薩", "狗狗", "阿狗", "老婆"])
    @commands.cooldown(rate=1, per=10, bucket=commands.Bucket.channel)
    async def wife(self, ctx: commands.Context, *message: str):
        '''修改指令回覆內容'''
        if ctx.message.channel.name== 'samoago':
            await ctx.channel.send("是我老婆")
            
    @commands.command(aliases= ["閃電", "傘電"])
    @commands.cooldown(rate=1, per=10, bucket=commands.Bucket.channel)
    async def samoago_lightning_command(self, ctx: commands.Context, *message: str):
        '''修改指令回覆內容'''
        if ctx.message.channel.name== 'samoago':
            await ctx.channel.send("https://clips.twitch.tv/FurryTolerantHorseTwitchRaid-CEV_PZijNwPka0-Z")
    
    @commands.command()
    @commands.cooldown(rate=1, per=10, bucket=commands.Bucket.channel)
    async def test_cmd(self, ctx: commands.Context, channel_name: str):
        '''取得頻道基本資訊'''
        if not self.check_channel(ctx): return
        msg= await self.bot.search_channels(channel_name, live_only= True)
        print(msg[0])
        game= await self.bot.fetch_games(ids= [msg[0].game_id])
        print(game[0])
        
        
def prepare(bot):
    bot.add_cog(Cmd(bot))