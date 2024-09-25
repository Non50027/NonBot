import gc
from . import event, error


def load(bot):
    
    event.load(bot)
    error.load(bot)
    
    # 準備完成
    @bot.event
    async def on_ready():
        print('Discord Bot - 頻道測試 ...')
        # 頻道測試
        # all guild
        for guild in bot.guilds:
            # 權限測試
            for channel in guild.channels:
                perms = channel.permissions_for(guild.me)
                if not perms.send_messages:
                    print(f'Discord Bot - 無法在 {guild.name} 的 {channel.name} 發訊息...')
                if not perms.read_message_history:
                    print(f'Discord Bot - 無法讀取 {guild.name} 中 {channel.name} 的歷史訊息...')
            
        print('Discord Bot - 頻道測試結束')
        
        print('Discord Bot - 準備完成')
    
    # 指令成功執行時觸發
    @bot.event
    async def on_command_completion(ctx):
        """
        指令成功執行時觸發
        """
        if ctx.guild is not None:
            print(f"指令 {ctx.command.qualified_name} 在 {ctx.guild.name} 被 {ctx.author.display_name} 執行")
        else:
            print(f"指令 {ctx.command.qualified_name} 被 {ctx.author} 執行")

        # 強制執行垃圾回收
        gc.collect()
