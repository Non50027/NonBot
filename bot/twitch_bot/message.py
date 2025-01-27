import twitchio, random, time, asyncio, requests, os
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
        self.temp_repeat_message= {}
        self.emoji_prefix_list= []
        self.bot.loop.create_task(self._init_start_task())
        self.emoji_prefix_list= [
                'zuoo84',
                'moko',
                'kspksp',
                'yuzumi6',
                'kirali502',
                'ddd2',
                'moondo25',
                'iiti',
                'mikiao',
                'fish6',
                'samoag',
                'reirei621',
                'migi',
                'yoruno8',
                'hibiki27',
            ]
    
    async def _init_start_task(self):
        await self.bot.wait_for_ready()
        task1 = asyncio.create_task(self._init_temp())
        task2 = asyncio.create_task(self.loop_task_response_message())
        # task3 = asyncio.create_task(self.get_emoji_prefix())

        await asyncio.gather(task1, task2)
    
        
    async def _init_temp(self):
        while True:
            self.temp_emoji= {}
            self.temp_repeat_message= {}
            await asyncio.sleep(5*60)
    
    async def loop_task_response_message(self):
        print('  \033[1;32m-\033[0m 開始 Twitch chat hello 自動回覆')
        while True:
            await asyncio.sleep(5)
            def filter_channel(ch_name, hello: bool)-> str:
                
                def choice_emoji_message(
                        key_word: str, 
                        hello_emoji_list: list[str]| None,
                        goodnight_emoji_list: list[str]| None= None,
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
                        key_word= 'reirei621',
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
                
                elif ch_name== 'zuoo846095':
                    return choice_emoji_message(
                        key_word= 'zuoo84',
                        hello_emoji_list= ['Anan', 'Love', 'GOGO', 'Fly', 'HIHI'],
                        hello_fill_word= 'Love',
                        goodnight_emoji_list= ['Smile'],
                        goodnight_fill_word= 'Love'
                    )
                return ''
            
            try:
                async def repeat_channels(numbers: dict, words: list, is_hi: bool):
                    for channel_name, users in numbers.items():
                        msg= random.choice(words)
                        msg= f" {' '.join(users)} {msg}"
                    
                        msg+= filter_channel(channel_name, is_hi)
                        ch= self.bot.get_channel(channel_name)
                        await ch.send(msg)
                await repeat_channels(
                    self.goodnight_msg,
                    ['晚灣', '晚ㄤ', '祝好夢', '晚安'],
                    False
                )
                await asyncio.sleep(3)
                await repeat_channels(
                    self.hi_msg,
                    ['早安呀', '早ㄤ', '早ㄤ呀', '早早', '早安'],
                    True
                )
                self.goodnight_msg.clear()
                self.hi_msg.clear()
            except Exception as e:
                print('task error', e)
            await asyncio.sleep(55)
            
        
        
        
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
        if message.author is None: 
            # print(f"{message.channel}->{message.content}... author is None")
            return
        # 檢查訊息內容是否包含自訂指令
        ctx = await self.bot.get_context(message)
        # 如果是指令
        if ctx.command:
            if message.channel.name!= 'pigeoncwc': return
            await self.bot.handle_commands(message)
            return
        
        
        
        # 排除自己 & bot
        if any(message.author.name== name for name in [self.bot.nick, 'nightbot', 'streamelements', 'moobot']): return
        
        try:
            await self.message_response(message)
            await self.repeat_message(message)
        except Exception as e:
            print('auto message error', e)
    
    async def message_response(self, message: twitchio.Message):
        if message.author.name== message.channel.name: return
        
        if not [_ for _ in ['大家', '各位', '農農', 'infinite0527'] if _ in message.content]: return
        
        if [_ for _ in ['農農', 'infinite0527'] if _ in message.content]:
            # 印出包含我的留言
            if len(message.content.split('@'))>2:
                _= f'@{len(message.content.split("@"))-1}個人 {" ".join(message.content.split("@")[-1].split(" ")[1:])}'  
            elif '@' in message.content: 
                _= ' '.join(message.content.split(' ')[1:])
            else: _= message.content
                
            print(f'\033[0;35m{datetime.now().strftime("%H:%M:%S")}\033[0m - \033[0;31m{message.channel.name}\033[0m -> \033[0;32m{message.author.display_name}\033[0m{message.author.name} : {_}')
            # non= self.bot.discord.get_user(482720097715093514)
            # ch_owner= await message.channel.user()
            # await non.send(f'{ch_owner.display_name}-> {message.author.display_name}: {_}')
        
        # 分類早安、晚安
        if any(_ in message.content.lower() for _ in ['晚安', '晚灣', 'moko114', 'bye']):
            if self.check_cooldowns(message.channel.name+ message.author.name+ '晚安', 30000): return
            
            if message.channel.name not in self.goodnight_msg:
                self.goodnight_msg[message.channel.name]= []
            self.goodnight_msg[message.channel.name].append(f'@{message.author.name}')
            
        elif any(_ in message.content.lower() for _ in ['早安', '安安', '早ㄤ', 'ㄤㄤ' , '早早', '早呀', 'hi', 'happy', 'mokoeee', 'mokoceng1', 'moko104', 'mokolily1', 'hoya', 'migiyaya', 'mumu', 'mokoola', 'mokoceng1', 'bell', 'ring', 'sheep', 'fish6an', 'iitiftb', 'iitinono', 'iiti00', 'iitiboo', 'idol', 'takesichicken', 'call', 'ddd2jump']):
            if self.check_cooldowns(message.channel.name+ message.author.name+ '安安', 30000): return
            
            if message.channel.name not in self.hi_msg:
                self.hi_msg[message.channel.name]= []
            self.hi_msg[message.channel.name].append(f'@{message.author.name}')
            
    # 刷一樣的回復
    async def repeat_message(self, message: twitchio.Message):
        '''
        當有連續一樣的x留言出現時跟著刷
        表符與文字的邏輯分開處理
        '''
        # 排除部分頻道
        if any(_== message.channel.name for _ in ['kannazukilubee', 'seki_meridian' ,'nemesisxdfp']): return
        # 排除部分關鍵字
        if any(_ in message.content for _ in ['@', '+1', 'Cheer']): return
        msg= None
        _content= message.content.split(' ')
        
        # if any(t in message.content for t in ['醬肉', '降落']):
        #     if self.check_cooldowns(message.channel.name+ 'emoji', 120): return
        #     await message.channel.send('歡迎醬肉~')
            
        if '歡回' in message.content:
            if self.check_cooldowns(message.channel.name+ 'welcome', 60*30): return
            await asyncio.sleep(5)
            await message.channel.send(message.content)
        # 表符
        # 判斷內容只有單一表符並且至少 2 個
        elif len(_content)> 1 and len(set(_content))== 1:
            # 只會使用我有訂閱的表符
            if not any(prefix in message.content for prefix in self.emoji_prefix_list): return
            
            # 將表符加入列表
            self.temp_emoji.setdefault(message.channel.name, [])
            self.temp_emoji[message.channel.name].append(_content[0])
            
            # 將較舊的內容自列表中刪除
            if len(self.temp_emoji[message.channel.name])> 3:
                self.temp_emoji[message.channel.name]= self.temp_emoji[message.channel.name][1:]
            elif len(self.temp_emoji[message.channel.name])<3: return
            
            # 一起刷並進入CD
            if len(set(self.temp_emoji[message.channel.name]))== 1 \
            and not self.check_cooldowns(message.channel.name+ 'emoji', 60):
                msg= f' {self.temp_emoji[message.channel.name][0]} '*random.randint(1,3)
                del self.temp_emoji[message.channel.name]
        # 文字
        else:
            if message.content.replace(' ', '').isalnum(): return
            # 將聊天室的留言加入列表
            self.temp_repeat_message.setdefault(message.channel.name, [])
            self.temp_repeat_message[message.channel.name].append(message.content)
            
            # 將較舊的留言自列表中刪除
            if len(self.temp_repeat_message[message.channel.name])> 3:
                self.temp_repeat_message[message.channel.name]= self.temp_repeat_message[message.channel.name][1:]
            elif len(self.temp_repeat_message[message.channel.name])<3: return
            
            # 判斷列表中元素是否全等 並加入CD
            if len(set(self.temp_repeat_message[message.channel.name]))== 1 \
                and not self.check_cooldowns(message.channel.name+ 'repeat', 100):
                    msg= self.temp_repeat_message[message.channel.name][0]
                    del self.temp_repeat_message[message.channel.name]
        if msg is None: return
        await asyncio.sleep(3)
        await message.channel.send(msg)
        
            
def prepare(bot):
    bot.add_cog(Message(bot))
