from datetime import datetime
import gc, os, discord, requests, dotenv, time, httpx
from discord.ext import commands
from discord_bot.tool import CogCore
from twitch_bot import Bot as TwitchBot

dotenv.load_dotenv()


class Event(CogCore):
    
    # 指令成功執行時觸發
    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        """
        指令成功執行時觸發
        """
        if ctx.guild is not None:
            print(f"指令 \033[0;36m{ctx.command.qualified_name}\033[0m 在 \033[0;31m{ctx.guild.name}\033[0m 被 \033[0;32m{ctx.author.display_name}\033[0m 執行")
        else:
            print(f"指令 \033[0;36m{ctx.command.qualified_name}\033[0m 被 \033[0;32m{ctx.author}\033[0m 執行")

        # 強制執行垃圾回收
        gc.collect()
    
    async def test_guild_channels(self, guild: discord.Guild):
        # 權限測試
        count= 0
        for channel in guild.channels:
            count+= 1
            print(f'       \033[0;31m{guild.name}\033[0m [ {count} / {len(guild.channels)} ]', end='\r')
            perms = channel.permissions_for(guild.me)
            if not perms.send_messages:
                print(f'\n      \033[1;32m-\033[0m 無法在 \033[0;34m{channel.name}\033[0m 發訊息...')
            if not perms.read_message_history:
                print(f'\n      \033[1;32m-\033[0m 無法讀取 \033[0;34m{channel.name}\033[0m 的歷史訊息...')
            if count== len(guild.channels):
                print()

    
    async def start_twitch_bot(self):
        
        response = requests.get(f"{os.getenv('VITE_BACKEND_DJANGO_URL')}/oauth/check_twitch_token/")
        # async with httpx.AsyncClient() as client:
        #     response = await client.get(f"{os.getenv('VITE_BACKEND_DISCORD_URL')}/oauth/validate")

        if response.status_code!=200:
            print("\nTwitch token 已過期，正在嘗試更新...(；´д｀)")
            try:
                # async with httpx.AsyncClient() as client:
                #     response= await client.get(f"{os.getenv('VITE_BACKEND_DISCORD_URL')}/oauth/refresh-twitch-token")
                response = requests.get(f"{os.getenv('VITE_BACKEND_DJANGO_URL')}/oauth/re_get_twitch_token/")
                
                if response.status_code!=200:
                    print(f"刷新 Twitch Token 失敗 (T_T) : {response}")
                    return
                response_data= response.json()
                del os.environ['TWITCH_BOT_TOKEN']
                del os.environ['TWITCH_BOT_REFRESH_TOKEN']
                dotenv.load_dotenv()
                print(f"Twitch Token 刷新成功 ヾ(＾∇＾)")
                print(f"新的時間為: \033[0;35m{time.strftime('%H: %M: %S', time.localtime( time.time()+ response_data['expires_in']))}\033[0m")
            except Exception as e:
                print('start check token error:', e)
        if self.bot.twitch is None:
            self.bot.twitch= TwitchBot(
                token= os.getenv('TWITCH_BOT_TOKEN'),
                discord_bot= self.bot
            )
            self.bot.loop.create_task(self.bot.twitch.start())
        else:
            print(f'\t\033[0;36mTwitch Bot\033[0m - 已登入帳號 | \033[0;32m{self.bot.twitch.nick}\033[0m')
    
    # 準備完成
    @commands.Cog.listener()
    async def on_ready(self):
        print('   \033[1;32m-\033[0m 開始頻道測試 ...')
        # 頻道測試
        # all guild
        for guild in self.bot.guilds:
            await self.test_guild_channels(guild)
        print('   \033[1;32m-\033[0m 頻道測試結束')
        print('  \033[1;32m-\033[0;36m 啟動完成\033[0m')
        
        await self.start_twitch_bot()
        # await self.bot.twitch.wait_for_ready()
        # _= LiveNotify(self.bot.twitch)
        # self.bot.loop.create_task(_.start_task())
        
    @commands.Cog.listener()
    async def on_disconnect(self):
        # print(f"\033[0;35m{datetime.now().strftime('%H:%M:%S')} \033[0m失去連線 ...")
        # await self.bot.twitch.close()
        # self.bot.twitch= None
        pass
    
    @commands.Cog.listener()
    async def on_resumed(self):
        # print(f"\033[0;35m{datetime.now().strftime('%H:%M:%S')} \033[0m重新連線")
        # print(f'\n\033[0;36mDiscord Bot\033[0m - 已登入帳號 | \033[0;32m{self.bot.user}\033[0m')
        # await self.start_twitch_bot()
        pass
        
async def setup(bot):
    await bot.add_cog(Event(bot))