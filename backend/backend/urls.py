from django.contrib import admin
from django.urls import path, include
import discord_bot.urls, twitch_bot.urls, oauth.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('discord/', include(discord_bot.urls)),
    path('twitch/', include(twitch_bot.urls)),
    path('oauth/', include(oauth.urls)),
]
