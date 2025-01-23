from fastapi import APIRouter, status, Depends, Request
from fastapi.responses import JSONResponse
from sqlmodel import Session, select
from ..models import Token, get_session
from ..tool import update_env_variable
import os, requests, dotenv, time
from fastapi_csrf_protect import CsrfProtect

router= APIRouter()


@router.get("/csrf-token")
def get_csrf(csrf_protect: CsrfProtect = Depends()):
    csrf_token = csrf_protect.generate_csrf()
    return {"csrfToken": csrf_token}

@router.post("/submit-form")
def submit_form(csrf_protect: CsrfProtect = Depends()):
    csrf_protect.validate_csrf(csrf_protect.get_csrf_from_headers())
    return {"message": "Form submitted successfully!"}

# 驗證
@router.get('/validate', status_code= 200)
async def validate_twitch_token():
    
    url= 'https://id.twitch.tv/oauth2/validate'
    
    dotenv.load_dotenv()
    
    headers = {'Authorization': f"Bearer {os.getenv('TWITCH_BOT_TOKEN')}"}  
    
    response= requests.get(url, headers= headers)
    response_data= response.json()
    
    if response.status_code==200:
        return JSONResponse(response_data, status_code= status.HTTP_200_OK)
    
    return JSONResponse(response_data, status_code= status.HTTP_401_UNAUTHORIZED)

@router.get('/twitch-client-token', status_code= 200)
async def get_twitch_token():
    data= {
        'client_id': os.getenv('TWITCH_BOT_ID'),
        'client_secret': os.getenv('TWITCH_BOT_SECRET'),
        'grant_type': 'client_credentials'
    }
    url= 'https://id.twitch.tv/oauth2/token'
    response= requests.post(url, data=data)
    if response.status_code==200:
        response_data= response.json()
        print(f"有效時間至: \033[0;35m{time.strftime('%H: %M: %S', time.localtime( time.time()+ response_data['expires_in']))}\033[0m")
        print(response_data)
        update_env_variable('TWITCH_BOT_TOKEN', response_data['access_token'])
        dotenv.load_dotenv()
        
        return JSONResponse(response_data, status_code= status.HTTP_200_OK)
    else:
        print('取得令牌失敗', response.status_code, response.text)
        return JSONResponse({'message':'取得令牌失敗', 'error': response.text}, status_code= status.HTTP_400_BAD_REQUEST)
    
@router.get('/twitch-user-token', status_code= 200)
async def get_twitch_token(code: str):
    data= {
        'client_id': os.getenv('TWITCH_BOT_ID'),
        'client_secret': os.getenv('TWITCH_BOT_SECRET'),
        'grant_type': 'authorization_code',
        'code': code,
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