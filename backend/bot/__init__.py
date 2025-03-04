import sys, os
from .bot_discord import Bot as DiscordBot
from .bot_twitch import Bot as TwitchAdminBot

sys.path.append(os.path.abspath(os.path.dirname(__file__)))