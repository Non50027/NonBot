from fastapi import FastAPI
from discord.ext import commands

app= FastAPI()

# 需要傳入 Discord Bot 的實例
discord_bot: commands.Bot= None

@app.get('/')
async def home():
    print('home')
    return {'message': 'OK'}

@app.get('/get_guilds')
async def get_name():
    print(0)
    global discord_bot
    if discord_bot is None: return {'error': 'bot is null ...'}
    print(discord_bot.guilds)
    return {'message': 'OK'}

# 初始化 Discord Bot 實例
def set_discord_bot(bot: commands.Bot):
    global discord_bot
    print('discord server init bot', bot)
    discord_bot = bot