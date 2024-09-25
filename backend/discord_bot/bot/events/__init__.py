import gc
from . import event, error


def load(bot):
    
    event.load(bot)
    error.load(bot)
    
    # 準備完成
    @bot.event
    async def on_ready():
        print('   \033[1;32m-\033[0m 開始頻道測試 ...')
        # 頻道測試
        # all guild
        for guild in bot.guilds:
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
            
        print('\n   \033[1;32m-\033[0m 頻道測試結束')
        
        print('  \033[1;32m-\033[0;36m 啟動完成\033[0m\n')
    
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
