import subprocess
from discord.ext import commands

class Api(commands.Cog):
    
    def __init__(self, bot):
        super().__init__()
        self.bot= bot
        self.uvicorn_process = None  # 儲存 Uvicorn
        
    @commands.Cog.listener()
    async def on_ready(self):
        """當 bot 準備好時，設置全域變數"""
        pass

    @commands.hybrid_command()
    @commands.is_owner()
    async def start_server(self, ctx: commands.Context):
        """啟動 Uvicorn 伺服器"""
        print('Discord 伺服器啟動中 ... ', end='')
        if self.uvicorn_process is not None:
            await ctx.send("伺服器已經在運行中")
            return
        
        # 啟動 Uvicorn 伺服器
        self.uvicorn_process = subprocess.Popen(
            [
                "uvicorn",
                "bots.discord_bot.bot.server.request:app",
                "--host",
                "0.0.0.0",
                "--port", 
                "7615", 
                "--reload",
                "--ssl-keyfile=D:\\DiscordBot\\NonBot\\non.com.tw.key",
                "--ssl-certfile=D:\\DiscordBot\\NonBot\\non.com.tw.pem"
            ],
            shell= False
        )
        print('OK')
        
        await ctx.send("伺服器已啟動", ephemeral= True)

    @commands.hybrid_command()
    @commands.is_owner()
    async def stop_server(self, ctx: commands.Context):
        """停止 Uvicorn 伺服器"""
        if self.uvicorn_process is None:
            await ctx.send("沒有正在運行的伺服器", ephemeral= True)
            return
        
        # 停止 Uvicorn 伺服器
        self.uvicorn_process.terminate()
        self.uvicorn_process = None
        await ctx.send("伺服器已停止", ephemeral= True)

    @commands.hybrid_command()
    @commands.is_owner()
    async def restart_server(self, ctx: commands.Context):
        """重啟 Uvicorn 伺服器"""
        if self.uvicorn_process is not None:
            # 如果伺服器在運行，先停止
            self.uvicorn_process.terminate()
            self.uvicorn_process = None
        
        # 重新啟動 Uvicorn
        self.uvicorn_process = subprocess.Popen(
            [
                "uvicorn", 
                "bots.discord_bot.bot.server.request:app", 
                "--host", 
                "0.0.0.0", 
                "--port", 
                "7615", 
                "--reload",
                "--ssl-keyfile=D:\\DiscordBot\\NonBot\\non.com.tw.key",
                "--ssl-certfile=D:\\DiscordBot\\NonBot\\non.com.tw.pem"
            ],
            shell= False
        )
        await ctx.send("伺服器已重新啟動", ephemeral= True)
    

async def setup(bot):
    await bot.add_cog(Api(bot))
    
