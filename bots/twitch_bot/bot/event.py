import twitchio, random, time, gc, asyncio
from datetime import datetime
from bot import CogCore
from twitchio.ext import commands


class Event(CogCore):
    def __init__(self, *args, **kwargs):
        super().__init__( *args, **kwargs)
        self.cooldowns= {}
        self.temp_emoji= {}
        self.hi_msg= {}
        self.goodnight_msg= {}
        

    # 確認 CD
    def check_cooldowns(self, user_name: str, cd: int) -> bool:
        '''
        user_name (str): 項目名
        cd (int): CD 秒數
        True is not CD
        False is CD
        '''
        current_time= time.time()
        last_used = self.cooldowns.get(user_name, 0)  # 取得用戶上次使用時間...默認 0

        # CD 中
        if current_time - last_used < cd:
            return True
        self.cooldowns[user_name] = current_time
        return False

    # 偵測聊天室訊息
    @commands.Cog.event()
    async def event_message(self, message: twitchio.Message):
        
        # 檢查 message.author 是否為 None
        # 這是由於我的BOT名稱跟我的名稱一樣引起的
        if message.author is None:
            return
        
        # 檢查訊息內容是否包含自訂指令
        ctx = await self.bot.get_context(message)
        # 如果是指令
        if ctx.command and message.author.name == self.bot.nick:
            await self.bot.handle_commands(message)
            return  
        
        # 排除自己
        if message.author.name == self.bot.nick:
            return
        
        # await self.birthday(message)
        await self.goodnight(message)
        await self.say_hi(message)
        await self.welcome(message)
        await self.emoji(message)
        
    # 自動回覆生日快樂
    async def birthday(self, message: twitchio.Message):
        if not ('我生日' in message.content and '今天' in message.content): return
            
        if self.check_cooldowns(message.channel.name+ message.author.name+ '生日', 3000): return
            
        await asyncio.sleep(5)
        await message.channel.send(f" @{message.author.name} 生日大快樂 mokoRiboon ")
        print(f'\033[0;35m{datetime.now().strftime("%H:%M:%S")}\033[0m - \033[0;31m{message.channel.name}\033[0m -> \033[0;32m{message.author.display_name}\033[0m : {message.content}')
        print(f'\033[0;35m{datetime.now().strftime("%H:%M:%S")}\033[0m - \033[0;31m{message.channel.name}\033[0m -> 回復 \033[0;32m{message.author.display_name}\033[0m 生快')
        
    # 自動回復晚安
    async def goodnight(self, message: twitchio.Message):
        cache= 27
        if not [_ for _ in ['大家', '各位', '農農'] if _ in message.content]: return
        if not [_ for _ in ['晚安', '晚安', 'moko114'] if _ in message.content]: return
        
        if not self.check_cooldowns(message.channel.name+ '晚安', cache):
            self.goodnight_msg.get(message.channel.name, '@'+message.author.name)
            return
        
        if message.channel.name in self.goodnight_msg.keys():
            self.goodnight_msg[message.channel.name]+= ' @'+message.author.name
            return
        
        if (time.time()-(self.cooldowns.get(message.channel.name+ '晚安', 0)))>=cache+1 and self.goodnight_msg.get(message.channel.name, "")!= '':
            if self.check_cooldowns(message.channel.name+ message.author.name+ '晚安', 3000): return
            
            msg= random.choice(['晚灣', '晚安', '祝好夢'])
            msg= f" {self.goodnight_msg[message.channel.name]} {msg}"
            self.goodnight_msg[message.channel.name]= ''
            
            if message.channel.name== 'hennie2001': msg+= ' moko114  mokoBebe '
            
            elif message.channel.name== 'kspksp': msg+= ' kspkspBye  kspkspSleep '
            
            elif message.channel.name== 'migi_tw': msg+= ' migi88  migiZZZZ '
            
            elif message.channel.name== 'test40228': msg+= ' fish6Bye  fish6Zz '
            
            elif message.channel.name== 'kirali_neon': msg+= ' kirali502888  kirali502Sleep '
            
            elif message.channel.name== 'reirei_neon': msg+= ' reirei17Zzz  reirei17Sweeep '
            
            elif message.channel.name== 'yuzumi_neon': msg+= ' yuzumi6Zz  yuzumi6Zzz '
            
            elif message.channel.name== 'earendelxdfp': msg+= ' ddd288  ddd2Heart '
            
            elif message.channel.name== 'iitifox': msg+= ' iitiPpr  iitiPr  iitiZzz '
            
            await message.channel.send(msg)
            # print(f'\033[0;35m{datetime.now().strftime("%H:%M:%S")}\033[0m - \033[0;31m{message.channel.name}\033[0m -> 回復 {msg}')
        
        
    # 自動回復安安
    async def say_hi(self, message: twitchio.Message):
        
        cache= 27
        
        if not '農農' in message.content: return
        # 印出包含我的留言
        _= f'@{len(message.content.split("@"))-1}個人 {" ".join(message.content.split("@")[-1].split(" ")[1:])}' if len(message.content.split('@'))>1 else message.content
        print(f'\033[0;35m{datetime.now().strftime("%H:%M:%S")}\033[0m - \033[0;31m{message.channel.name}\033[0m -> \033[0;32m{message.author.display_name}\033[0m{message.author.name} : {_}')
            
        # 不包含內容 跳出
        if not any(_ in message.content for _ in ['早安', '安安', '早ㄤ' , '早早', '早呀', 'mokoHi1', 'mokoHIhi', 'migiHoya', 'migiYAYA', 'mokoOLA', 'mokoCeng1', 'mokoSheep1', 'fish6An', 'fish6Hi', 'iitiFTB', 'iitiNONO', 'iiti00']): return
        
        
        if not self.check_cooldowns(message.channel.name+ '安安', cache):
            self.hi_msg.get(message.channel.name, '@'+message.author.name)
            return
        
        if message.channel.name in self.hi_msg.keys():
            self.hi_msg[message.channel.name]+= ' @'+message.author.name
            return
        
        # 計算並判斷CD
        if (time.time()-(self.cooldowns.get(message.channel.name+ '安安', 0)))>= cache+1 and self.hi_msg.get(message.channel.name, "")!= '':
            if self.check_cooldowns(message.channel.name+ message.author.name+ '安安', 3000): return
                
            msg= random.choice(['早安呀', '早ㄤ', '早ㄤ呀', '早早', '早安'])
            msg= f" {self.hi_msg[message.channel.name]} {msg}"
            self.hi_msg[message.channel.name]= ''
            
            if message.channel.name== 'hennie2001': # msg+= ' mokoHIhi  mokoFlower '
                _= random.choice(['mokoHi1', 'moko53', 'mokoDance', 'mokoHAPPY2', 'mokoCeng1'])
                msg+= f' {_}  mokoLove '
            
            elif message.channel.name== 'migi_tw': msg+= ' migiHoya  migiLOVE2 '
                
            elif message.channel.name== 'kspksp': msg+= ' kspkspHorn  kspkspLove '
            
            elif message.channel.name== 'test40228': msg+= ' fish6Hihi  fish6Heart '
                
            elif message.channel.name== 'kirali_neon': msg+= ' kirali502Hello  kirali502Heart '
            
            elif message.channel.name== 'reirei_neon': msg+= ' reirei17Hi  reirei17Heart '
            
            elif message.channel.name== 'yuzumi_neon': msg+= ' yuzumi6Hi  yuzumi6Heart '
                
            elif message.channel.name== 'earendelxdfp': msg+= ' ddd2Hi  ddd2Heart '
                
            elif message.channel.name== 'iitifox': msg+= ' iitiHii  iitiLove '
                
            await message.channel.send(msg)
            # print(f'\033[0;35m{datetime.now().strftime("%H:%M:%S")}\033[1;32m - \033[0;31m{message.channel.name}\033[0m -> 回復 : {msg} ')
        
        
    # 跟著歡回
    async def welcome(self, message: twitchio.Message):
        if not message.content.startswith('歡回'):
            return
            
        if not self.check_cooldowns(message.channel.name+ '歡回temp', 10):
            self.temp_welcome_msg= message.content
            return
        
        if not self.check_cooldowns(message.channel.name+ '歡回', 600):
            await asyncio.sleep(5)
            await message.channel.send(self.temp_welcome_msg)
            print(f'\033[0;35m{datetime.now().strftime("%H:%M:%S")}\033[0m - \033[0;31m{message.channel.name}\033[0m -> {message.content}')
        
    # 一起刷表符
    async def emoji(self, message: twitchio.Message):
        
        # 判斷內容只有單一表服並且至少3個
        _= message.content.split(' ')
        if not (len(_)> 1 and len(set(_))== 1): return
            
        # 判斷是否為我能用的表服
        temp= [ 'moko', 'fish', 'kspksp', 'migi', 'iiti', 'kirali', 'yuzumi', 'reirei', 'samoag', 'mikiao', 'hantea', 'ddd2', 'abdd1223']
        if not any([_[0].startswith(__) for __ in temp]): return
        
        # 儲存表符並開始計時10秒
        if not self.check_cooldowns(message.channel.name+ 'temp_emoji', 10):
            self.temp_emoji.get(message.channel.name, _[0])
            return

        # 不一樣的表符就跳出
        if _[0]!= self.temp_emoji.get(message.channel.name, ''):
            self.temp_emoji[message.channel.name]= _[0]
            return
        
        # 一起刷並進入CD
        if not self.check_cooldowns(message.channel.name+ 'emoji', 20):
            await asyncio.sleep(3)
            msg= self.temp_emoji[message.channel.name]*3 if self.temp_emoji[message.channel.name]=='7' else self.temp_emoji[message.channel.name]
            await message.channel.send(f' {msg} '*random.randint(1,3))
            self.temp_emoji[message.channel.name]= ''
            
            
    # 指令執行後觸發...無論指令是否失敗
    @commands.Cog.event()
    async def global_after_invoke(ctx: commands.Context):
        """
        指令執行後觸發...無論指令是否失敗
        """
        print(f"\033[0;35m{datetime.now().strftime('%H:%M:%S')}\033[0m - 指令 {ctx.command.name} 在 {ctx.channel.name} 被 {ctx.author.name} 執行")
        
        # 強制執行垃圾回收
        gc.collect()
        
def setup(bot):
    bot.add_cog(Event(bot))