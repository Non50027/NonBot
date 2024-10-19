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
        self.loop_task_response_message.start()
        
    
    @tasks.loop(minutes= 1)
    async def loop_task_response_message(self):
        await asyncio.sleep(5)
        
        def filter_channel(ch_name, hello: bool)-> str| None:
            
            def choice_emoji_message(key_word: str, emoji_list: list[str], fill_word: str|None= None, fill_word_site: bool= True)-> str:
                '''
                若有 emoji_list 則從 emoji_list 中隨機抽取 1-2個可以重複的表符
                然後若不選擇 fill_word 則會在只抽出一個的情況下重複表符
                最後會輸出 2個表符 | None
                
                key_word: 表符前綴
                emoji_list: 要回復的表符列表
                fill_word: 填充用的表符
                fill_word_site: 填充表符的填充位置...預設為後面
                '''
                choice_emoji= random.choices(emoji_list, k= random.randint(1, 2))
                if fill_word is None:
                    choice_emoji= choice_emoji if len(choice_emoji)>1 else choice_emoji* 2
                elif fill_word_site:
                    choice_emoji= choice_emoji if len(choice_emoji)>1 else choice_emoji+[fill_word]
                else:
                    choice_emoji= choice_emoji if len(choice_emoji)>1 else [fill_word]+choice_emoji
                return ''.join([' '+key_word+emoji+' ' for emoji in choice_emoji])
            
            if ch_name== 'hennie2001':
                if hello:
                    return choice_emoji_message(
                        'moko',
                        ['Hi1', '53', 'Dance', 'HAPPY2', 'Ceng1', '101', '100', '104', '106', '107', '116', '120', '125', 'Bell', 'Luo3', 'Sheep1', 'RouRou', 'Sheep5', 'Te'],
                        'Love'
                    )
                else: return ' moko114  mokoBebe '
            
            elif ch_name== 'kspksp':
                if hello:
                    return choice_emoji_message(
                        'kspksp',
                        ['Love', 'Jump', 'Horn', 'Bell', 'Hi', 'Lick', 'Jump', 'Lovely', 'Move', 'Press', 'Wink'],
                    )
                else:
                    return choice_emoji_message(
                        'kspksp',
                        ['Sleep', 'Sleeping', 'Tired', 'XX', 'Dead', 'Bed', 'Bye'],
                        'Bye',
                        False
                    )
            
            elif ch_name== 'qttsix':
                if hello: return ' qttRub  qttHeart '
                else: return ' qttSleep '
            
            elif ch_name== 'migi_tw':
                if hello:
                    return choice_emoji_message(
                        'migi',
                        ['Haoya', 'HIHI', 'Hoya', 'Lick', 'UWU', 'YAYA'],
                        random.choice(['LOVE2', 'Milove'])
                    )
                else: 
                    return choice_emoji_message(
                        'migi',
                        ['LAZY', 'MUMU', 'HUGG', 'Papa', 'XX', 'ZZZZ'],
                        '88',
                        False
                    )
            
            elif ch_name== 'test40228':
                if hello:
                    return choice_emoji_message(
                        'fish6',
                        ['Hihi', '0U0', 'Heart', 'An', 'Happy']
                    )
                else:
                    return choice_emoji_message(
                        'fish6',
                        ['Xx', 'Zz', '0U0', 'HUG', 'Heart'],
                        'Bye',
                        False
                    )
                
            elif ch_name== 'kirali_neon':
                if hello:
                    return choice_emoji_message(
                        'kirali502',
                        ['Bigface', 'Aba', 'Hello', 'CLAP', 'Desk', 'Jump', 'Ring', 'Unicorn', 'Wiggle', 'Hehehe'],
                        'Heart'
                    )
                else:
                    return choice_emoji_message(
                        'kirali502',
                        ['Deadge', 'Kiralivanish', 'Pull', '888', 'Sleep'],
                    )
            
            elif ch_name== 'reirei_neon':
                if hello:
                    return choice_emoji_message(
                        'reirei17',
                        ['Catshake', 'Clap', 'Hi', 'Luvpotato', 'Riiiing', 'Shake', 'Shy', 'Weeeee', 'Slaptable', 'Unicorn'],
                        'Heart'
                    )
                else:
                    return choice_emoji_message(
                        'reirei17',
                        ['Rip', 'Bye', 'Tremble', 'Vanish', 'Zzz', 'Sweeep'],
                        'Bye',
                        False
                    )
            
            elif ch_name== 'yuzumi_neon':
                if hello:
                    return choice_emoji_message(
                        'yuzumi6',
                        ['JumpRolling', 'Dance', 'Hi', 'Nenene', 'Ring', 'Yure', 'Wiggle', 'Unicorn', 'Waku'],
                        'Heart'
                    )
                else:
                    return choice_emoji_message(
                        'yuzumi6',
                        ['Deadge', 'Peepovanish1', 'Zz', 'Zzz'],
                    )
                
            elif ch_name== 'hibiki_meridianproject':
                if hello:
                    return choice_emoji_message(
                        'hibiki27',
                        ['HI', 'Eatpopcorn', 'Dino', 'CHU'],
                        'Love'
                    )
                else:
                    return ' hibiki27Rub  hibiki27BYE '
                
            elif ch_name== 'yoruno_moonlit':
                if hello: return ' yoruno8Hihi  yoruno8Socute '
                else: return ' yoruno8Sleepp  yoruno8Sleepp '
            
            elif ch_name== 'earendelxdfp':
                if hello:
                    return choice_emoji_message(
                        'ddd2',
                        ['Ring', 'Heart', 'Hi', 'Jumpjump', 'Jump', 'Why', 'Shake', 'Shakey'],
                        'Heart'
                    )
                else:
                    return choice_emoji_message(
                        'ddd2',
                        ['Die', 'Gg', '88'],
                    )
            
            elif ch_name== 'iitifox':
                if hello:
                    return choice_emoji_message(
                        'iiti',
                        ['00', 'CUTE', 'Flap', 'Hiii', 'Hii', 'Pq', 'Pr', 'Ring', 'TT1', 'TT2'],
                        random.choice(['Loveu', 'Loveuu', 'Love'])
                    )
                else: return ' iitiZzz  iitiZzz '
            
            elif ch_name== 'moondogs_celestial':
                if hello: return ' moondo25LOVE  moondo25Happy '
                else: return ' moondogs_celestial  moondogs_celestial '
            
            elif ch_name== 'mikiaoboshi':
                if hello:
                    return choice_emoji_message(
                        'mikiao',
                        ['Ayaya', 'Brother', 'Bla', 'Chu', 'Crab', 'Dance', 'Hearts', 'Hi', 'Yaaaa'],
                        'Lovely'
                    )
                else: ''
            
            elif ch_name== 'samoago':
                if hello: 
                    return choice_emoji_message(
                        'samoagO',
                        ['BearFat', 'child', 'hi', 'flower', 'thumb', 'wave'],
                        'heart'
                    )
                else: return ' samoagOwarm  samoagOwarm '
                
            elif ch_name== '7a7a_o':
                if hello: return ' fafababyHi  fafababyL '
                else: return ' fafababyBaba '
        
            elif ch_name== 'hipudding1223':
                if hello: 
                    return choice_emoji_message(
                        'abdd1223',
                        ['Duai', 'Hello', 'VD'],
                        'Kiss'
                    )
                else: return ' abdd1223Sleep '
            return ''
                
        for key in self.hi_msg.keys():
            msg= random.choice(['早安呀', '早ㄤ', '早ㄤ呀', '早早', '早安'])
            msg= f" {self.hi_msg[key]} {msg}"
            
            msg+= filter_channel(key, True)
            ch= self.bot.get_channel(key)            
            await ch.send(msg)
        self.hi_msg= {}
        
        for key in self.goodnight_msg.keys():
            msg= random.choice(['晚灣', '晚ㄤ', '祝好夢', '晚安'])
            msg= f" {self.goodnight_msg[key]} {msg}"
        
            msg+= filter_channel(key, False)
            ch= self.bot.get_channel(key)
            await ch.send(msg)
        self.goodnight_msg= {}
        
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
            _= f'@{len(message.content.split("@"))-1}個人 {" ".join(message.content.split("@")[-1].split(" ")[1:])}' if len(message.content.split('@'))>2 else ' '.join(message.content.split(' ')[1:])
            print(f'\033[0;35m{datetime.now().strftime("%H:%M:%S")}\033[0m - \033[0;31m{message.channel.name}\033[0m -> \033[0;32m{message.author.display_name}\033[0m{message.author.name} : {_}')
            non= self.bot.discord.get_user(482720097715093514)
            try:
                ch_owner= await message.channel.user()
                await non.send(f'{ch_owner.display_name}-> {message.author.display_name}: {_}')
            except Exception as e:
                print('dc_send error', e)
        
        if message.author.name== 'Nightbot': return
        if message.author.name== 'StreamElements': return
        # 分類早安、晚安
        if any(_ in message.content.lower() for _ in ['晚安', '晚安', '晚灣', 'moko114', 'bye']):
            if self.check_cooldowns(message.channel.name+ message.author.name+ '晚安', 30000): return
            
            if self.check_cooldowns(message.channel.name+ '晚安', cache):
                self.goodnight_msg.get(message.channel.name, ' @'+message.author.name)
            else:
                self.goodnight_msg[message.channel.name]= '@'+message.author.name
            
        elif any(_ in message.content.lower() for _ in ['早安', '安安', '早ㄤ' , '早早', '早呀', 'hi', 'happy', 'moko104', 'hoya', 'migiyaya', 'mumu', 'mokoola', 'mokoceng1', 'bell', 'ring', 'sheep', 'fish6an', 'iitiftb', 'iitinono', 'iiti00']):
            if self.check_cooldowns(message.channel.name+ message.author.name+ '安安', 30000): return
            
            if self.check_cooldowns(message.channel.name+ '安安', cache):
                self.hi_msg.get(message.channel.name, ' @'+message.author.name)
            else:
                self.hi_msg[message.channel.name]= '@'+message.author.name
            
            
    # 跟著歡回
    async def welcome(self, message: twitchio.Message):
        if not message.content.startswith('歡回'): return
            
        if not self.check_cooldowns(message.channel.name+ '歡回temp', 10):
            self.temp_welcome_msg= message.content
            return
        
        if not self.check_cooldowns(message.channel.name+ '歡回', 600):
            await asyncio.sleep(5)
            await message.channel.send(self.temp_welcome_msg)
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
        if not self.check_cooldowns(message.channel.name+ 'emoji', 20):
            
            await asyncio.sleep(3)
            msg= self.temp_emoji[message.channel.name]*3 if self.temp_emoji[message.channel.name]=='7' else self.temp_emoji[message.channel.name]
            await message.channel.send(f' {msg} '*random.randint(1,3))
            del self.temp_emoji[message.channel.name]
            
def setup(bot):
    bot.add_cog(Message(bot))
