import discord, requests, dotenv, os, json, aiohttp, urllib3
from discord.ext import commands, tasks
from bot.serve import checkTwitchToken

dotenv.load_dotenv()
# 忽略 InsecureRequestWarning 警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Task(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.twitch= {
            'id': os.getenv('VITE_TWITCH_BOT_ID'),
            'time': checkTwitchToken()['expires_in'] if checkTwitchToken() else 900
        }
        self.refreshUrl= f"{os.getenv('VITE_BACKEND_URL')}/oauth/re_get_twitch_token/"
        self.bot.loop.create_task(self.start_task_init())

    async def start_task_init(self):
        await self.bot.wait_until_ready()
        self.on_live.start()
        print('     \033[1;32m-\033[0m 開始 直播偵測')
        self.check_twitch_token.start()
        print('     \033[1;32m-\033[0m 開始 Twitch Bot Token 偵測')
    
    @staticmethod
    async def fetch_twitch_data(url, headers):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                response= await response.json()
                return response if response else None
    
    @tasks.loop(minutes=5)
    async def check_twitch_token(self):
        
        self.twitch['time'] -= 300  # 每次檢查後剩餘時間減少60秒（1分鐘）

        # 如果剩餘時間小於5分鐘，則刷新Token
        if self.twitch['time'] <= 300:  # 300秒 = 5分鐘
            try:
                print("刷新 Twitch Token ...")
                response = requests.get(self.refreshUrl, verify=False)
                responseData= response.json()
                if response.status_code == 200:
                    self.twitch['time'] = responseData['expires_in']  # 更新新的有效期
                    print(f"新的時間為", self.twitch['time'])
                    print("Twitch Token 刷新成功")
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
            try:
                liveLists= await Task.fetch_twitch_data(url+userId, headers)
            except Exception as e:
                print('on_live error ', e)
                return
            
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
                liveUrl= f"https://www.twitch.tv/{liveData['user_login']}"
                embed.url= liveUrl
                
                img= f"https://static-cdn.jtvnw.net/previews-ttv/live_user_{liveData['user_login']}.jpg"
                embed.set_image(url= img)
                    
                embed.set_author(
                        name= liveData['user_name'],
                        url= liveUrl,
                        icon_url= subChannel['icon_url']
                        )
                embed.add_field(name= '分類', value= liveData['game_name'], inline= False)
                
                
                tag= f'<@&{subChannel["role"]}>' if subChannel['role'] is not None else ''
                
                ch= self.bot.get_channel(subChannel['channel'])
                await ch.send(tag, embed= embed)
                
                print(f"\033[0;32m{liveData['user_name']}\033[0m 在紫色學校開台了")
        
        # save json
        with open(jsonPath, 'w', encoding='utf8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
            
        
async def setup(bot):
    await bot.add_cog(Task(bot))
