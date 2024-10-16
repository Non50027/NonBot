from fastapi import FastAPI, Depends
from discord.ext import commands
from discord_bot import get_bot

app= FastAPI()
discord_bot= None

# 檢查 Bot 是否已經啟動
def get_discord_bot()->commands.Bot:
    global discord_bot
    discord_bot= get_bot()
    return discord_bot

@app.get('/guild')
async def get_guild(discord_bot: commands.Bot = Depends(get_discord_bot)):
    print(discord_bot.name,'46')
    return {'guild': 'mst'}

@app.get('/user')
async def get_guild():
    return {'user': 'non'}