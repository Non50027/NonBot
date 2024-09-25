import os, requests

# ck twitch bot token
def ckToken()-> bool:
    url= 'https://id.twitch.tv/oauth2/validate'
    token= os.getenv('TWITCH_BOT_TOKEN')
    headers = {
    'Authorization': f'Bearer {token}'
    }   
    response= requests.get(url, headers= headers)
    data= response.json()
    if response.status_code==200:
        return True
    else:
        print('twitch token 失效', data['status'], data['message'])
        return False