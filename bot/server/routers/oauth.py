from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
from sqlmodel import Session, select
from ..models import Token, get_session
from ..tool import update_env_variable
import os, requests, dotenv, time


router= APIRouter()

# 驗證
@router.get('/validate', status_code= 200)
async def validate_twitch_token():
    url= 'https://id.twitch.tv/oauth2/validate'
    
    headers = {'Authorization': f"Bearer {os.getenv('TWITCH_BOT_TOKEN')}"}  
    
    response= requests.get(url, headers= headers)
    response_data= response.json()
    
    if response.status_code==200:
        return JSONResponse(response_data, status_code= status.HTTP_200_OK)
    
    return JSONResponse(response_data, status_code= status.HTTP_401_UNAUTHORIZED)

# # 更新 .env 中的值
# def update_env_variable(key, new_value):
#     # 讀取現有的 .env 檔案內容
    
#     file_path= os.path.join(os.path.dirname(__file__).split('\\bot')[0], '.env')
#     with open(file_path, "r") as file:
#         lines = file.readlines()
        
#     # 準備寫入的內容
#     updated_lines = []
#     found = False

#     for line in lines:
#         # 去掉空白及換行
#         stripped_line = line.strip()
#         # 如果這一行是我們要更新的變數
#         if stripped_line.startswith(f"{key}="):
#             # 更新該變數的值
#             updated_lines.append(f"{key}={new_value}\n")
#             found = True
#         else:
#             # 保留其他的變數
#             updated_lines.append(line)

#     # 如果變數不存在，則新增一行
#     if not found:
#         updated_lines.append(f"{key}={new_value}\n")
        
#     # 將更新後的內容寫回 .env 檔案
#     with open(file_path, "w") as file:
#         file.writelines(updated_lines)

@router.post('/get-twitch-token', status_code= 200)
async def get_twitch_token(code: str):
    data= {
        'client_id': os.getenv('VITE_TWITCH_BOT_ID'),
        'client_secret': os.getenv('TWITCH_BOT_SECRET'),
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': f'https://non.com.tw/'
    }
    url= 'https://id.twitch.tv/oauth2/token'
    response= requests.post(url, data=data)
    if response.status_code==200:
        response_data= response.json()
        print(f"有效時間至: \033[0;35m{time.strftime('%H: %M: %S', time.localtime( time.time()+ response_data['expires_in']))}\033[0m")
        update_env_variable('TWITCH_BOT_TOKEN', response_data['access_token'])
        update_env_variable('TWITCH_BOT_REFRESH_TOKEN', response_data['refresh_token'])
        dotenv.load_dotenv()
        
        return JSONResponse(response_data, status_code= status.HTTP_200_OK)
    else:
        print('取得令牌失敗', response.status_code, response.text)
        return JSONResponse({'message':'取得令牌失敗', 'error': response.text}, status_code= status.HTTP_400_BAD_REQUEST)

@router.post('/token')
async def seve_token(requests_data: Token, session: Session = Depends(get_session)):
    # 檢查是否已有該用戶的 Token
    db_data = session.exec(select(Token).where(Token.id == requests_data.id)).first()
    
    if db_data:
        session.commit()
        return JSONResponse(
            content= {"error": "已有資料" },
            status_code= status.HTTP_502_BAD_GATEWAY
        )
    # 新增 Token
    session.add(requests_data)
    session.commit()
    return JSONResponse(
        content= {"message": "Token saved successfully!"},
        status_code= status.HTTP_200_OK
    )

@router.put('/token')
async def update_token(requests_data: Token, session: Session = Depends(get_session)):
    # 檢查是否已有該用戶的 Token
    db_data = session.exec(select(Token).where(Token.id == requests_data.id)).first()
    
    if db_data:
        # 更新 Token
        db_data.name = requests_data.name
        db_data.login = requests_data.login
    session.commit()
    return {"message": "Token saved successfully!"}

# 重新取得 token
@router.get('/refresh-twitch-token')
async def re_get_twitch_token():
    
    url= 'https://id.twitch.tv/oauth2/token'
    
    headers={'Content-Type': 'application/x-www-form-urlencoded'}
    
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': os.getenv('TWITCH_BOT_REFRESH_TOKEN'),
        'client_id': os.getenv('VITE_TWITCH_BOT_ID'),
        'client_secret': os.getenv('TWITCH_BOT_SECRET'),
    }
    response= requests.post(url, headers= headers, data= data)
    response_data= response.json()
    
    if response.status_code== 200:
        response_data= response.json()
        update_env_variable('TWITCH_BOT_TOKEN', response_data['access_token'])
        update_env_variable('TWITCH_BOT_REFRESH_TOKEN', response_data['refresh_token'])
        # 在重新加載前，手動刪除舊的環境變數
        del os.environ['TWITCH_BOT_TOKEN']
        del os.environ['TWITCH_BOT_REFRESH_TOKEN']
        dotenv.load_dotenv()
        return JSONResponse(response_data, status_code= status.HTTP_200_OK)
    else:
        print('twitch token 刷新失敗', response_data['status'], response_data['error'], response_data['message'])
        return JSONResponse(response_data, status_code= status.HTTP_400_BAD_REQUEST)