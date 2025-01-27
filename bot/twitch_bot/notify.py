import asyncio, os, dotenv
from datetime import datetime, timedelta
from twitch_bot.tool import CogCore

dotenv.load_dotenv()

class Notify(CogCore):
    def __init__(self, *args, **kwargs):
        super().__init__( *args, **kwargs)
        self.db_channels: list[dict]= []
        self.bot.loop.create_task(self._init_start_task())
    
    async def _init_start_task(self):
        await self.bot.wait_for_ready()
        task1 = asyncio.create_task(self.get_all_sub())
        task2 = asyncio.create_task(self.on_live())

        await asyncio.gather(task1, task2)
        
    async def get_all_sub(self):
        while True:
            url= f"{os.getenv('BACKEND_URL')}/twitch/all-sub-channel"
            self.db_channels= await self.get_data(url)
            
            await asyncio.sleep(60*60)
    
    async def on_live(self):
        
        print('  \033[1;32m-\033[0m 開始 twitch live 偵測')
        on_task= True
        while on_task:
            
            user_ids= [_['id'] for _ in self.db_channels]
            streams= await self.bot.fetch_streams(user_ids= user_ids)
            
            for sub in self.db_channels:
                if sub['id'] not in [_.user.id for _ in streams]: 

                    videos= await self.bot.fetch_videos(user_id= sub["id"])
                    video=videos[0]

                    data= {
                        'user_id': sub['id'],
                        'title': video.title,
                        'url': video.url,
                    }
                    url= f"{os.getenv('BACKEND_URL')}/discord/stop-live"
                    
                    await self.get_data(url, data)
                    continue
                
                stream= [
                    {
                        'id': _.user.id,
                        'video_id': _.id,
                        'name': _.user.name,
                        'title': _.title,
                        'started_at': _.started_at.isoformat(),
                        'viewer_count': _.viewer_count,
                        'game': _.game_name,
                        'thumbnail_url': _.thumbnail_url
                    } for _ in streams if _.user.id == sub['id']
                ][0]
                
                data= {
                    "login": sub["login"],
                    "background_url": sub["background_url"],
                    "icon_url": sub["icon_url"]
                }
                data.update(stream)
                
                url= f"{os.getenv('BACKEND_URL')}/discord/start-live"
                await self.get_data(url, data)
            
            await asyncio.sleep(60)
        else:
            print(' \033[1;32m- \033[0;31m結束 twitch live 偵測\033[0m')
        

    
def prepare(bot):
    bot.add_cog(Notify(bot))