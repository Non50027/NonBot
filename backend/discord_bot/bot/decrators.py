import json, os
from functools import wraps

class MyDecorators():
        
    @staticmethod
    def readJson(jsonFileName: str):
        '''
        讀取資料作為參數傳給裝飾的方法使用
        並將加工後的資料存回去
        
        讀取data中json檔
        jsonFileName (str): 檔案名稱
        '''
        def inner(functionName):
            
            # 繼承方法原來的狀態
            @wraps(functionName)
            async def wrapper(self, *args, **kwargs):
                
                # read json
                with open(os.path.join(os.path.dirname(__file__), f'data\\{jsonFileName}.json'), 'r', encoding='utf8') as file:
                    data= json.load(file)
                
                '''
                hybrid_command方法無法直接接收 dict 參數
                也不接收寫入kwargs
                也由於需要裝飾的方法有可能會擁有像是 ctx 這種限定位置的引數
                所以直接加入到 self中
                也應為這樣只能裝飾
                '''
                self.data= data
                result = await functionName(self, *args, **kwargs)
                
                # save json
                with open(os.path.join(os.path.dirname(__file__), f'data\\{jsonFileName}.json'), 'w', encoding='utf8') as file:
                    json.dump(result, file, ensure_ascii=False, indent=4)
                    
            return wrapper
        return inner