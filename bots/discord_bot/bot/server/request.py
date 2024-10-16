from fastapi import FastAPI
# from bots.discord_bot.bot.server import bot_

app= FastAPI()

@app.get('/get_bot_name')
async def get_name():
    print()
    return {'message': f'OK'}