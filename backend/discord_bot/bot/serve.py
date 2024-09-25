import requests, os, dotenv, aiohttp

dotenv.load_dotenv()

def checkTwitchToken()-> dict| bool:
    url= 'https://id.twitch.tv/oauth2/validate'
        
    headers = {
    'Authorization': f"Bearer {os.getenv('TWITCH_BOT_TOKEN')}"
    }   
    response= requests.get(url, headers= headers)
    data= response.json()
    if response.status_code==200:
        return data
    else:
        return False
    
async def fetch_twitch_data(url, headers):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            response= await response.json()
            return response if response else None