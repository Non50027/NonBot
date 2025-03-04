import os, orjson
from functools import wraps
from twitchio.ext import commands

class MyDecorators():
    
    @staticmethod
    def api_headers(function_name):
        '''
        連接API時使用的 headers settings
        並存在 self.headers
        '''
        @wraps(function_name)
        async def inner(self, ctx: commands.Context, *args, **kwargs):
            headers = {
                'Client-ID': os.getenv('VITE_TWITCH_BOT_ID'),
                'Authorization': f"Bearer {os.getenv('TWITCH_BOT_TOKEN')}"
            }
            self.headers= headers
            await function_name(self, ctx, *args, **kwargs)
        
        return inner

    
    @staticmethod
    def readJson(json_filename: str):
        '''
        讀取資料作為參數傳給裝飾的方法使用
        並將加工後的資料存回去
        
        讀取data中json檔
        json_filename (str): 檔案名稱
        '''
        def inner(function_name):
            
            # 繼承方法原來的狀態
            @wraps(function_name)
            async def wrapper(self, *args, **kwargs):
                # read json
                file_path= os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data' , f'{json_filename}.json')
                with open(file_path, 'rb') as file:
                    json_data= orjson.load(file.read())
                '''
                hybrid_command方法無法直接接收 dict 參數
                也不接收寫入kwargs
                也由於需要裝飾的方法有可能會擁有像是 ctx 這種限定位置的引數
                所以直接加入到 self中
                也應為這樣只能裝飾
                '''
                self.json_data= json_data
                result = await function_name(self, *args, **kwargs)
                
                if result is None: return
                # save json
                with open(file_path, 'wb') as file:
                    file.write(orjson.dump(result, option=orjson.OPT_INDENT_2))
                    
                self.json_data= None
                
            return wrapper
        return inner