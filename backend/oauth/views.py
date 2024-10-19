from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.middleware.csrf import get_token
import dotenv, os, requests, time
from django.conf import settings
from rest_framework import status
from tool import update_env_variable


@api_view(['GET'])
def get_csrf_token(request):
    csrf_token = get_token(request)
    return Response({'csrf_token': csrf_token})

@api_view(['POST'])
def get_twitch_token(request):
    if 'code' in request.data.keys():
        data= {
            'client_id': os.getenv('VITE_TWITCH_BOT_ID'),
            'client_secret': os.getenv('TWITCH_BOT_SECRET'),
            'code': request.data['code'],
            'grant_type': 'authorization_code',
            'redirect_uri': f'https://non.com.tw/'
        }
        url= 'https://id.twitch.tv/oauth2/token'
        response= requests.post(url, data=data)
        if response.status_code==200:
            response_data= response.json()
            print(f"有效時間為 {time.strftime('%H: %M: %S', time.gmtime((response_data['expires_in'])))}")
            update_env_variable('TWITCH_BOT_TOKEN', response_data['access_token'])
            update_env_variable('TWITCH_BOT_REFRESH_TOKEN', response_data['refresh_token'])
            dotenv.load_dotenv()
            return Response(response_data)
        else:
            print('取得令牌失敗', response.status_code, response.text)
            return Response({'message':'取得令牌失敗', 'error': response.text})

# 重新取得 token
@api_view(['GET'])
def re_get_twitch_token(request):
    
    client_id= os.getenv('VITE_TWITCH_BOT_ID')
    client_secret= os.getenv('TWITCH_BOT_SECRET')
    refresh_token= os.getenv('TWITCH_BOT_REFRESH_TOKEN')
    
    url= 'https://id.twitch.tv/oauth2/token'
    
    headers={'Content-Type': 'application/x-www-form-urlencoded'}
    
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': client_id,
        'client_secret': client_secret,
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
        return Response(response_data, status= status.HTTP_200_OK)
    else:
        print('twitch token 刷新失敗', response_data['status'], response_data['error'], response_data['message'])
        return Response(response_data)

@api_view(['GET'])
def check_twitch_token(request):
    url= 'https://id.twitch.tv/oauth2/validate'
    
    # 在重新加載前，手動刪除舊的環境變數
    headers = {'Authorization': f"Bearer {os.getenv('TWITCH_BOT_TOKEN')}"}  
    
    response= requests.get(url, headers= headers)
    response_data= response.json()
    
    if response.status_code==200:
        return Response(response_data, status= status.HTTP_200_OK)
    else:
        return Response(response_data, status= status.HTTP_401_UNAUTHORIZED)