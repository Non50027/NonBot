import discord, json, os, requests, dotenv, aiohttp
from discord.ext import commands

dotenv.load_dotenv()

class Live(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def fetch_twitch_data(url, headers):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                response= await response.json()
                return response if response else None
    
    @commands.hybrid_command()
    async def on_live(self, ctx: commands.Context):
        user_id='197367758'
        headers = {
            'Authorization': f"Bearer {os.getenv('TWITCH_BOT_TOKEN')}",
            'Client-Id': os.getenv('VITE_TWITCH_BOT_ID'),
        }
        url= f'https://api.twitch.tv/helix/streams?user_id='
        
        jsonPath= os.path.join(os.path.dirname(os.path.dirname(__file__)),'data\\subLive.json')
        # read json
        with open(jsonPath, 'r', encoding='utf8') as file:
            data= json.load(file)
        try:
            
            for subChannels in data.values():
                liveLists= await Live.fetch_twitch_data(url+user_id, headers)
                print(liveLists)
                
                if liveLists['data']==[]:
                    await ctx.send('no live')
                    return
                
                for subChannel in subChannels['twitch']:
                    
                    # 未在直播
                    if subChannel['id'] not in [_['id'] for _ in liveLists['data']]:
                        subChannel['live']= 'False'
                        continue
                        
                    # 已有開始直播的標籤...避免重複通知
                    if subChannel['live']== 'True':
                        continue
                    
                    # 加上直播中標籤
                    subChannel['live']= 'True'
                    
                    liveData= [_ for _ in liveLists['data'] if _['id']== subChannel['id']][0]
                    
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
        
        except Exception as e:
            print('error', e)
        
        print('直播偵測系統運作中...', end='\r')
        # save json
        with open(jsonPath, 'w', encoding='utf8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

async def setup(bot):
    await bot.add_cog(Live(bot))
