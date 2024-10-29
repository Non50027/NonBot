import twitchio, random, time, asyncio
from datetime import datetime
from twitchio.ext import commands
from discord.ext import tasks
from twitch_bot.tool import CogCore

class Message(CogCore):
    def __init__(self, bot, *args, **kwargs):
        super().__init__(bot, *args, **kwargs)
        self.cooldowns= {}
        self.temp_emoji= {}
        self.hi_msg= {}
        self.goodnight_msg= {}
        self.start_task()
    
    def start_task(self):
        if self.loop_task_response_message.is_running():
            self.loop_task_response_message.restart()
        else:
            self.loop_task_response_message.start()
    
    @tasks.loop(minutes= 1)
    async def loop_task_response_message(self):
        
        def filter_channel(ch_name, hello: bool)-> str:
            
            def choice_emoji_message(
                    key_word: str, 
                    hello_emoji_list: list[str]| None,
                    goodnight_emoji_list: list[str]| None,
                    hello_fill_word: str|None= None, hello_fill_word_site: bool= True,
                    goodnight_fill_word: str|None= None, goodnight_fill_word_site: bool= True,
                )-> str:
                '''
                若有 emoji_list 則從 emoji_list 中隨機抽取 1-2個可以重複的表符
                然後若不選擇 fill_word 則會在只抽出一個的情況下重複表符
                最後會輸出 2個表符 | None
                
                key_word: 表符前綴
                emoji_list: 要回復的表符列表
                fill_word: 填充用的表符
                fill_word_site: 填充表符的填充位置...預設為後面
                '''
                if hello:
                    if hello_emoji_list is None: return ''
                    choice_emoji= random.choices(hello_emoji_list, k= random.randint(1, 2))
                    if len(choice_emoji)>1:
                        choice_emoji= choice_emoji
                    elif hello_fill_word is None:
                        choice_emoji= choice_emoji* 2
                    elif hello_fill_word_site:
                        choice_emoji= choice_emoji+[hello_fill_word]
                    else:
                        choice_emoji= [hello_fill_word]+choice_emoji
                else:
                    if goodnight_emoji_list is None: return ''
                    choice_emoji= random.choices(goodnight_emoji_list, k= random.randint(1, 2))
                    if len(choice_emoji)>1:
                        choice_emoji= choice_emoji
                    elif goodnight_fill_word is None:
                        choice_emoji= choice_emoji* 2
                    elif goodnight_fill_word_site:
                        choice_emoji= choice_emoji+[goodnight_fill_word]
                    else:
                        choice_emoji= [goodnight_fill_word]+choice_emoji
                
                return ''.join([' '+key_word+emoji+' ' for emoji in choice_emoji])
            
            if ch_name== 'hennie2001':
                return choice_emoji_message(
                    key_word= 'moko',
                    hello_emoji_list= ['Hi1', '53', 'Dance', 'HAPPY2', 'Ceng1', '101', '100', '104', '106', '107', '116', '120', '125', 'Bell', 'Luo3', 'Sheep1', 'RouRou', 'Sheep5', 'Te'],
                    hello_fill_word= 'Love',
                    goodnight_emoji_list= ['114', 'Bebe']
                )
            
            elif ch_name== 'infinite0527':
                if hello: return 'testHI'
                else: return 'testGoodNight'
            
            elif ch_name== 'kspksp':
                return choice_emoji_message(
                    key_word= 'kspksp',
                    hello_emoji_list= ['Love', 'Jump', 'Horn', 'Bell', 'Hi', 'Lick', 'Jump', 'Lovely', 'Move', 'Press', 'Wink'],
                    goodnight_emoji_list= ['Sleep', 'Sleeping', 'Tired', 'XX', 'Dead', 'Bed', 'Bye'],
                    goodnight_fill_word= 'Bye',
                    goodnight_fill_word_site= False
                )
            
            elif ch_name== 'qttsix':
                if hello: return ' qttRub  qttHeart '
                else: return ' qttSleep '
            
            elif ch_name== 'migi_tw':
                return choice_emoji_message(
                    key_word= 'migi',
                    hello_emoji_list= ['Haoya', 'HIHI', 'Hoya', 'Lick', 'UWU', 'YAYA'],
                    hello_fill_word= random.choice(['LOVE2', 'Milove']),
                    goodnight_emoji_list= ['LAZY', 'MUMU', 'HUGG', 'Papa', 'XX', 'ZZZZ'],
                    goodnight_fill_word= '88',
                    goodnight_fill_word_site= False
                )
            
            elif ch_name== 'test40228':
                return choice_emoji_message(
                    key_word= 'fish6',
                    hello_emoji_list= ['Hihi', '0U0', 'Heart', 'An', 'Happy'],
                    goodnight_emoji_list= ['Xx', 'Zz', '0U0', 'HUG', 'Heart'],
                    goodnight_fill_word= 'Bye',
                    goodnight_fill_word_site= False
                )
                
            elif ch_name== 'kirali_neon':
                return choice_emoji_message(
                    key_word= 'kirali502',
                    hello_emoji_list= ['Bigface', 'Aba', 'Hello', 'CLAP', 'Desk', 'Jump', 'Ring', 'Unicorn', 'Wiggle', 'Hehehe'],
                    hello_fill_word= 'Heart',
                    goodnight_emoji_list= ['Deadge', 'Pull', '888', 'Sleep'],
                )
            
            elif ch_name== 'reirei_neon':
                return choice_emoji_message(
                    key_word= 'reirei17',
                    hello_emoji_list= ['Catshake', 'Clap', 'Hi', 'Luvpotato', 'Riiiing', 'Shake', 'Shy', 'Weeeee', 'Slaptable', 'Unicorn'],
                    hello_fill_word= 'Heart',
                    goodnight_emoji_list= ['Rip', 'Bye', 'Tremble', 'Zzz', 'Sweeep'],
                    goodnight_fill_word= 'Bye',
                    goodnight_fill_word_site= False
                )
            
            elif ch_name== 'yuzumi_neon':
                return choice_emoji_message(
                    key_word= 'yuzumi6',
                    hello_emoji_list= ['JumpRolling', 'Dance', 'Hi', 'Nenene', 'Ring', 'Yure', 'Wiggle', 'Unicorn', 'Waku'],
                    hello_fill_word= 'Heart',
                    goodnight_emoji_list= ['Deadge', 'Zz', 'Zzz'],
                )
                
            elif ch_name== 'hibiki_meridianproject':
                return choice_emoji_message(
                    key_word= 'hibiki27',
                    hello_emoji_list= ['HI', 'Eatpopcorn', 'Dino', 'CHU'],
                    hello_fill_word= 'Love',
                    goodnight_emoji_list= ['Rub', 'BYE']
                )
                
            elif ch_name== 'yoruno_moonlit':
                if hello: return ' yoruno8Hihi  yoruno8Socute '
                else: return ' yoruno8Sleepp  yoruno8Sleepp '
            
            elif ch_name== 'earendelxdfp':
                return choice_emoji_message(
                    key_word= 'ddd2',
                    hello_emoji_list= ['Ring', 'Heart', 'Hi', 'Jumpjump', 'Jump', 'Why', 'Shake', 'Shakey'],
                    hello_fill_word= 'Heart',
                    goodnight_emoji_list= ['Die', 'Gg', '88'],
                )
            
            elif ch_name== 'iitifox':
                return choice_emoji_message(
                    key_word= 'iiti',
                    hello_emoji_list= ['00', 'CUTE', 'Flap', 'Hiii', 'Hii', 'Pq', 'Pr', 'Ring', 'TT1', 'TT2'],
                    hello_fill_word= random.choice(['Loveu', 'Loveuu', 'Love']),
                    goodnight_emoji_list= ['Zzz', 'Zzz']
                )
            
            elif ch_name== 'moondogs_celestial':
                if hello: return ' moondo25LOVE  moondo25Happy '
                else: return ' moondo25Ohno  moondo25Ohno '
            
            elif ch_name== 'mikiaoboshi':
                return choice_emoji_message(
                    key_word= 'mikiao',
                    hello_emoji_list= ['Ayaya', 'Brother', 'Bla', 'Chu', 'Crab', 'Dance', 'Hearts', 'Hi', 'Yaaaa'],
                    hello_fill_word= 'Lovely'
                )
            
            elif ch_name== 'samoago':
                    return choice_emoji_message(
                        key_word= 'samoagO',
                        hello_emoji_list= ['BearFat', 'child', 'hi', 'flower', 'thumb', 'wave'],
                        hello_fill_word= 'heart',
                        goodnight_emoji_list= ['warm', 'warm']
                    )
                
            elif ch_name== '7a7a_o':
                if hello: return ' fafababyHi  fafababyL '
                else: return ' fafababyBaba '
        
            elif ch_name== 'hipudding1223':
                return choice_emoji_message(
                    key_word= 'abdd1223',
                    hello_emoji_list= ['Duai', 'Hello', 'VD'],
                    hello_fill_word= 'Kiss',
                    goodnight_emoji_list= ['Sleep', 'Sleep']
                )
            return ''
                
        for channel_name, users in self.goodnight_msg.items():
            msg= random.choice(['晚灣', '晚ㄤ', '祝好夢', '晚安'])
            msg= f" {' '.join(users)} {msg}"
        
            msg+= filter_channel(channel_name, False)
            ch= self.bot.get_channel(channel_name)
            await ch.send(msg)
        self.goodnight_msg.clear()
        
        await asyncio.sleep(5)
        for channel_name, users in self.hi_msg.items():
            msg= random.choice(['早安呀', '早ㄤ', '早ㄤ呀', '早早', '早安'])
            msg= f" {' '.join(users)} {msg}"
            
            msg+= filter_channel(channel_name, True)
            ch= self.bot.get_channel(channel_name)            
            await ch.send(msg)
        self.hi_msg.clear()
        
        
    @loop_task_response_message.before_loop
    async def loop_task_response_message_is_ready(self):
        print('     \033[1;32m-\033[0m 開始 Twitch chat hello 自動回覆')
        
    @loop_task_response_message.after_loop
    async def loop_task_response_message_is_close(self):
        print('     \033[1;32m-\033[0m 結束 Twitch chat hello 自動回覆')
    
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
        if current_time - last_used < cd: return True
        
        self.cooldowns[user_name] = current_time
        return False
    
    # 偵測聊天室訊息
    @commands.Cog.event()
    async def event_message(self, message: twitchio.Message):
        
        # 檢查 message.author 是否為 None
        # 這是由於我的BOT名稱跟我的名稱一樣引起的
        if message.author is None: return
        
        # 檢查訊息內容是否包含自訂指令
        ctx = await self.bot.get_context(message)
        # 如果是指令
        if ctx.command and message.author.name == self.bot.nick:
            await self.bot.handle_commands(message)
            return  
        
        # 排除自己
        if message.author.name == self.bot.nick: return
        try:
            await self.message_response(message)
            await self.welcome(message)
            await self.emoji(message)
        except Exception as e:
            print('auto message error', e)
    
    async def message_response(self, message: twitchio.Message):
        cache= 27
        
        if not [_ for _ in ['大家', '各位', '農農', 'infinite0527'] if _ in message.content]: return
        
        if '農農' in message.content:
            # 印出包含我的留言
            if len(message.content.split('@'))>2:
                _= f'@{len(message.content.split("@"))-1}個人 {" ".join(message.content.split("@")[-1].split(" ")[1:])}'  
            elif '@' in message.content: 
                _= ' '.join(message.content.split(' ')[1:])
            else: _= message.content
                
            print(f'\033[0;35m{datetime.now().strftime("%H:%M:%S")}\033[0m - \033[0;31m{message.channel.name}\033[0m -> \033[0;32m{message.author.display_name}\033[0m{message.author.name} : {_}')
            non= self.bot.discord.get_user(482720097715093514)
            ch_owner= await message.channel.user()
            await non.send(f'{ch_owner.display_name}-> {message.author.display_name}: {_}')
        
        if message.author.name== 'Nightbot': return
        if message.author.name== 'StreamElements': return
        # 分類早安、晚安
        if any(_ in message.content.lower() for _ in ['晚安', '晚安', '晚灣', 'moko114', 'bye']):
            if self.check_cooldowns(message.channel.name+ message.author.name+ '晚安', 30000): return
            
            if message.channel.name not in self.goodnight_msg:
                self.goodnight_msg[message.channel.name]= []
            self.goodnight_msg[message.channel.name].append(f'@{message.author.name}')
            
        elif any(_ in message.content.lower() for _ in ['早安', '安安', '早ㄤ', 'ㄤㄤ' , '早早', '早呀', 'hi', 'happy', 'mokoeee', 'moko104', 'mokolily1', 'hoya', 'migiyaya', 'mumu', 'mokoola', 'mokoceng1', 'bell', 'ring', 'sheep', 'fish6an', 'iitiftb', 'iitinono', 'iiti00', 'idol', 'takesichicken']):
            if self.check_cooldowns(message.channel.name+ message.author.name+ '安安', 30000): return
            
            if message.channel.name not in self.hi_msg:
                self.hi_msg[message.channel.name]= []
            self.hi_msg[message.channel.name].append(f'@{message.author.name}')
            
            
    # 跟著歡回
    async def welcome(self, message: twitchio.Message):
        if '歡回' not in message.content: return
            
        if not self.check_cooldowns(message.channel.name+ '歡回temp', 10): return
        
        if not self.check_cooldowns(message.channel.name+ '歡回', 600):
            await asyncio.sleep(5)
            await message.channel.send(message.content)
            print(f'\033[0;35m{datetime.now().strftime("%H:%M:%S")}\033[0m - \033[0;31m{message.channel.name}\033[0m -> {message.content}')
        
    # 一起刷表符
    async def emoji(self, message: twitchio.Message):
        # 判斷內容只有單一表服並且至少 2 個
        _= message.content.split(' ')
        if not (len(_)> 1 and len(set(_))== 1): return
        
        # 判斷是否為我能用的表服
        temp= [
            'moko', 'qtt', 'fish', 'migi', 'iiti', 'samoag', 'mikiao',
            'ksp', 'kirali', 'yuzumi', 'reirei', 'hibiki27', 'yoruno8',
            'ddd2', 'moondo', 'hantea', 'abdd1223', 'fafababy'
            ]
        if not any([_[0].startswith(__) for __ in temp]): return
        
        # 儲存表符並開始計時10秒
        if not self.check_cooldowns(message.channel.name+ 'temp_emoji', 20):
            self.temp_emoji.get(message.channel.name, _[0])
            return
        
        # 不一樣的表符就跳出
        if _[0]!= self.temp_emoji.get(message.channel.name):
            self.temp_emoji[message.channel.name]= _[0]
            return
        
        # 一起刷並進入CD
        if not self.check_cooldowns(message.channel.name+ 'emoji', 30):
            
            await asyncio.sleep(3)
            msg= self.temp_emoji[message.channel.name]*3 if self.temp_emoji[message.channel.name]=='7' else self.temp_emoji[message.channel.name]
            await message.channel.send(f' {msg} '*random.randint(1,3))
            del self.temp_emoji[message.channel.name]
            
def prepare(bot):
    bot.add_cog(Message(bot))

'''
烟花正在跟 “ REX 肯特 虧皮 小鹽“ 一起玩【 瓦 】♡
'''