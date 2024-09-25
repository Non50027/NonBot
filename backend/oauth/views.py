from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.middleware.csrf import get_token
import dotenv, os, requests
from django.conf import settings
from rest_framework import status
from tool import update_env_variable

dotenv.load_dotenv()

@api_view(['GET'])
def get_csrf_token(request):
    csrf_token = get_token(request)
    return Response({'csrfToken': csrf_token})

@api_view(['POST'])
def getTwitchToken(request):
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
            responseData= response.json()
            print(f'有效時間為 {responseData["expires_in"]} 秒')
            update_env_variable('TWITCH_BOT_TOKEN', responseData['access_token'])
            update_env_variable('TWITCH_BOT_REFRESH_TOKEN', responseData['refresh_token'])
            return Response(responseData)
        else:
            print('取得令牌失敗', response.status_code, response.text)
            return Response({'message':'取得令牌失敗', 'error': response.text})

# 重新取得 token
@api_view(['GET'])
def reGetTwitchToken(request):
    client_id= os.getenv('VITE_TWITCH_BOT_ID')
    client_secret= os.getenv('TWITCH_BOT_SECRET')
    refresh_token= os.getenv('TWITCH_BOT_REFRESH_TOKEN')
    url= 'https://id.twitch.tv/oauth2/token'
    headers={
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
    'grant_type': 'refresh_token',
    'refresh_token': refresh_token,
    'client_id': client_id,
    'client_secret': client_secret,
    }
    response= requests.post(url, headers= headers, data= data)
    responseData= response.json()
    if response.status_code== 200:
        responseData= response.json()
        update_env_variable('TWITCH_BOT_TOKEN', responseData['access_token'])
        update_env_variable('TWITCH_BOT_REFRESH_TOKEN', responseData['refresh_token'])
        return Response(responseData, status= status.HTTP_200_OK)
    else:
        print('twitch token 刷新失敗', responseData['status'], responseData['error'], responseData['message'])
        return Response(responseData)
