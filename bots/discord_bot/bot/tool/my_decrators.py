import json, os
from functools import wraps

class MyDecorators():
    
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
                with open(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), f'data\\{json_filename}.json'), 'r', encoding='utf8') as file:
                    json_data= json.load(file)
                '''
                hybrid_command方法無法直接接收 dict 參數
                也不接收寫入kwargs
                也由於需要裝飾的方法有可能會擁有像是 ctx 這種限定位置的引數
                所以直接加入到 self中
                也應為這樣只能裝飾
                '''
                self.json_data= json_data
                result = await function_name(self, *args, **kwargs)
                
                if self.json_data is None: return
                # save json
                with open(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), f'data\\{json_filename}.json'), 'w', encoding='utf8') as file:
                    json.dump(result, file, ensure_ascii=False, indent=4)
                    
            return wrapper
        return inner