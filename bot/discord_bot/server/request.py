from fastapi import FastAPI, Depends
from discord.ext import commands
from discord_bot import get_bot

app= FastAPI()
# 需要傳入 Discord Bot 的實例
discord_bot: commands.Bot= None

# 檢查 Bot 是否已經啟動
def get_discord_bot()->commands.Bot:
    global discord_bot
    discord_bot= get_bot()
    return discord_bot

@app.get('/')
async def home():
    print('home')
    return {'message': 'OK...'}

@app.get('/get_guilds')
async def get_name(bot: commands.Bot = Depends(get_discord_bot)):
    print(bot.guilds)
    return {'message': 'OK'}

# 初始化 Discord Bot 實例
@app.get('/get_bot')
def get_discord_bot(bot: commands.Bot = Depends(get_discord_bot)):
    print('server to discord bot', bot)
    # return {'discord bot': bot.get_user(482720097715093514)}
    return {'discord bot': 'ok'}