import discord, os
from discord.ext import commands
from bot_discord.tool import CogCore
from discord import app_commands

class LiveNotify(CogCore):
    
    @commands.hybrid_command()
    @commands.is_owner()
    @app_commands.describe(channel_url= '圖奇頻道網址', channel_id= '要通知的頻道ID')
    async def sub_twitch(self, ctx: commands.Context, channel_url: str, channel_id: str):
        if 'twitch' in channel_url:
            twitch_name= channel_url.split('twitch.tv/')[1]
        else:
            twitch_name= channel_url
            channel_url= f"https://www.twitch.tv/{twitch_name}"
            
        url= f"{os.getenv('BACKEND_URL')}/twitch/channel/{twitch_name}"
        twitch_channel= await self.post_data(url)
        
        url= f"{os.getenv('BACKEND_URL')}/discord/sub-twitch/{channel_id}/{twitch_channel['id']}"
        await self.post_data(url)
        
        discord_channel= self.bot.get_channel(int(channel_id))
        
        embed= discord.Embed()
        embed.title= "訂閱成功"
        embed.description= f"已訂閱 {twitch_channel['display_name']} 的直播\n將會在 {discord_channel.mention} 通知"
        embed.color= discord.Color.green()
        embed.url= channel_url
        embed.set_image(url= twitch_channel['background_url'])
        embed.set_author(
            name= twitch_channel['display_name'],
            url= channel_url,
            icon_url= twitch_channel['icon_url']
        )
        await ctx.send(embed= embed)

    @commands.hybrid_command()
    @commands.is_owner()
    async def test_command(self, ctx: commands.Context, channel_id: str):
        channel= self.bot.get_channel(int(channel_id))
        print(channel)
        await ctx.send("OK", ephemeral= True)

async def setup(bot):
    await bot.add_cog(LiveNotify(bot))

