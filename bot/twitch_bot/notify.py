import asyncio
from datetime import datetime, timedelta
from twitch_bot.tool import CogCore


class Notify(CogCore):
    def __init__(self, *args, **kwargs):
        super().__init__( *args, **kwargs)
        self.db_channels: list[dict]= []
        self.bot.loop.create_task(self._init_start_task())
    
    async def _init_start_task(self):
        await self.bot.wait_for_ready()
        task1 = asyncio.create_task(self.get_channel_name())
        task2 = asyncio.create_task(self.on_live())

        await asyncio.gather(task1, task2)
        
    async def get_channel_name(self):
        while True:
            url= 'https://api.non.com.tw/twitch/all-sub-channel'
            self.db_channels= await self.get_data(url)
            await asyncio.sleep(8*60*60)
    
    async def on_live(self):
        print('   \033[1;32m-\033[0m 開始 twitch live 偵測')
        on_task= True
        while on_task:
            for channel in self.db_channels: 
                live_channel= await self.bot.search_channels(channel['login'], live_only= True)
                live_channel= [_ for _ in live_channel if _.name== channel['login']]
                
                if live_channel== []: continue
                live_channel= live_channel[0]
                try:
                    if (datetime.now()- (live_channel.started_at+ timedelta(hours= 8))) > timedelta(seconds= 63): continue
                except Exception as e:
                    print(channel['display_name'], 'live error', e)
                    print(live_channel)
                    continue

                game= await self.bot.fetch_games([live_channel.game_id])
                game= game[0]

                url= f'https://api.non.com.tw/discord/notify'
                data= {
                    'id': live_channel.id,
                    'login': live_channel.name,
                    'display_name': live_channel.display_name if live_channel.display_name else live_channel.name,
                    'title': live_channel.title,
                    'game': game.name
                }
                
                print(f"\033[0;35m{datetime.now().strftime('%H:%M:%S')}\033[0m - \033[0;32m{data['display_name']}\033[0m 開台了~")
                
                await self.get_data(url, data= data)
                    
            await asyncio.sleep(60)
        else:
            print(' \033[1;32m- \033[0;31m結束 twitch live 偵測\033[0m')
        

    
def prepare(bot):
    bot.add_cog(Notify(bot))