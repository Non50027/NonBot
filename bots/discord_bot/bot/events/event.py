import discord, gc
from discord.ext import commands
from bot.tool import CogCore


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
    
    # 準備完成
    @commands.Cog.listener()
    async def on_ready(self):
        print('   \033[1;32m-\033[0m 開始頻道測試 ...')
        # 頻道測試
        # all guild
        for guild in self.bot.guilds:
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
        print('   \033[1;32m-\033[0m 頻道測試結束')
        
        print('  \033[1;32m-\033[0;36m 啟動完成\033[0m')
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        print(f'{member.display_name}偷偷D滑了進來!')
        await self.bot.get_channel(1246368178762809475).send(f'歡迎{member.mention}的降落~')

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        print(f'{member.display_name}偷偷D離大家遠去了!')
        await self.bot.get_channel(1246368590316175440).send(f'{member.display_name}偷偷D離大家遠去了...')    
    
async def setup(bot):
    await bot.add_cog(Event(bot))