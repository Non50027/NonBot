from fastapi import FastAPI
from server.routers import discord, oauth


app = FastAPI()

app.include_router(router= discord.router, prefix='/discord')
app.include_router(router= oauth.router, prefix='/oauth')
