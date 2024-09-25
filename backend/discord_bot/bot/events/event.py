    
def load(bot):
    
    # 成員加入伺服器
    @bot.event
    async def on_member_join(member):
        print(f'{member.display_name}偷偷D滑了進來!')
        await bot.get_channel(1246368178762809475).send(f'歡迎{member.mention}的降落~')

    # 成員離開伺服器
    @bot.event
    async def on_member_remove(member):
        print(f'{member.display_name}偷偷D離大家遠去了!')
        await bot.get_channel(1246368590316175440).send(f'{member.display_name}偷偷D離大家遠去了...')    
    
    # 回復關鍵字
    async def respond_message(message):
        
        if "哈哈哈" in message.content:
            msg= "笑屁笑"
        elif "笨烏龜" in message.content:
            msg= "你兇我( ´•̥̥̥ω•̥̥̥` )"
        elif "閉嘴" in message.content:
            msg= "இдஇ"
        elif '@小烏龜' in message.content:
            msg= '安抓 ~'            
        elif "智障烏龜" in message.content:
            msg= "我又不是故意的(;´༎ຶД༎ຶ`)"
        else:
            return
        
        await message.channel.send(msg)