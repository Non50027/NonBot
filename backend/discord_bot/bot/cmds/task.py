import discord, requests, dotenv, os, json, aiohttp
from discord.ext import commands, tasks

dotenv.load_dotenv()

class Task(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.twitch= {
            'id': os.getenv('VITE_TWITCH_BOT_ID'),
            'time': 3600
        }
        self.refreshUrl= f"{os.getenv('VITE_BACKEND_URL')}/oauth/re_get_twitch_token/"
        self.bot.loop.create_task(self.start_task_init())

    async def start_task_init(self):
        await self.bot.wait_until_ready()
        self.on_live.start()
        print('開始直播偵測')
        self.check_twitch_token.start()
        print('開始 Twitch Token 偵測')
    
    @staticmethod
    async def fetch_twitch_data(url, headers):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                response= await response.json()
                return response if response else None
    
    @tasks.loop(minutes=5)
    async def check_twitch_token(self):
        
        self.twitch['time'] -= 300  # 每次檢查後剩餘時間減少60秒（1分鐘）
        print('twitch token 剩餘時間', self.twitch['time'])
        # 如果剩餘時間小於5分鐘，則刷新Token
        if self.twitch['time'] <= 300:  # 300秒 = 5分鐘
            try:
                print("刷新 Twitch Token ...")
                response = requests.get(self.refreshUrl, verify=False)
                if response.status_code == 200:
                    print("Twitch Token 刷新成功")
                    # 假設API回應中有新的 expires_in 值，你可以更新它
                    token_info = response.json()
                    self.twitch['time'] = token_info['expires_in']  # 更新新的有效期
                else:
                    print(f"刷新 Twitch Token 失敗: {response}")
            except Exception as e:
                print('error', e)
    
    @tasks.loop(seconds= 30)
    async def on_live(self):
        headers = {
            'Authorization': f"Bearer {os.getenv('TWITCH_BOT_TOKEN')}",
            'Client-Id': self.twitch['id'],
        }
        url= f'https://api.twitch.tv/helix/streams?user_id='
        
        jsonPath= os.path.join(os.path.dirname(os.path.dirname(__file__)),'data\\subLive.json')
        # read json
        with open(jsonPath, 'r', encoding='utf8') as file:
            data= json.load(file)
            
        for subChannels in data.values():
            subUserId= [_['id'] for _ in subChannels['twitch']]
            userId= '&user_id='.join(subUserId)
            liveLists= await Task.fetch_twitch_data(url+userId, headers)
            for subChannel in subChannels['twitch']:
                
                # 未在直播
                if subChannel['id'] not in [_['user_id'] for _ in liveLists['data']]:
                    subChannel['live']= 'False'
                    continue
                    
                # 已有開始直播的標籤...避免重複通知
                if subChannel['live']== 'True':
                    continue
                
                # 加上直播中標籤
                subChannel['live']= 'True'
                
                liveData= [_ for _ in liveLists['data'] if _['user_id']== subChannel['id']][0]
                
                embed= discord.Embed()
                embed.title= liveData['title']
                embed.color= 0x9700d0    #9700d0
                embed.url= f"https://www.twitch.tv/{subChannel['name']}"
                
                img= f'https://static-cdn.jtvnw.net/previews-ttv/live_user_{subChannel["name"]}.jpg'
                embed.set_image(url= img)
                    
                embed.set_author(
                        name= subChannel['display_name'],
                        url= url,
                        icon_url= subChannel['icon_url']
                        )
                embed.add_field(name= '分類', value= liveData['game_name'], inline= False)
                
                
                tag= f'<@&{subChannel["role"]}>' if subChannel['role'] is not None else ''
                
                ch= self.bot.get_channel(subChannel['channel'])
                await ch.send(tag, embed= embed)
                
                print(subChannel['display_name'], '在紫色學校開台了')
        
        print('直播偵測系統運作中...', end='\r')
        # save json
        with open(jsonPath, 'w', encoding='utf8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
            
        
async def setup(bot):
    await bot.add_cog(Task(bot))
