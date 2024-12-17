from fastapi import FastAPI
from server.routers import api_discord, api_twitch, oauth 
import asyncio

app = FastAPI()

app.include_router(router= oauth.router, prefix='/oauth')
app.include_router(router= api_discord.router, prefix='/discord')
app.include_router(router= api_twitch.router, prefix='/twitch')
