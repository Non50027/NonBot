from fastapi import FastAPI
from server.routers import discord


app = FastAPI()

app.include_router(router= discord.router, prefix='/discord')
