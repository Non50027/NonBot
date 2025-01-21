import aiohttp, discord, os
from discord.ext import commands
from discord import app_commands
from discord_bot.tool import CogCore

class Message(CogCore):

    # Bot附讀
    @commands.hybrid_command(description= '讓bot 說話')
    @app_commands.describe(msg= '想讓小烏龜說甚麼?')
    async def say(self, ctx: commands.Context, *, msg: str):
        '''
        讓 bot 說話 使用 \n 換行
        '''
        msg= '\n'.join(msg.split(r'\n'))
        await ctx.send(msg)
        
    @commands.hybrid_command()
    @commands.is_owner()
    @app_commands.describe(msg= '想讓小烏龜說甚麼?')
    async def private_message(self, ctx: commands.Context, user_id: str, *, msg: str):
        '''
        讓 bot 說話 使用 \n 換行
        '''
        msg= '\n'.join(msg.split(r'\n'))
        await self.bot.get_user(int(user_id)).send(msg)
        
    @commands.hybrid_command()
    async def last_msg(self, ctx: commands.Context, msg_id: str, m: str):
        msg= await ctx.channel.fetch_message(int(msg_id))
        embed= msg.embeds[0]
        # embed= discord.Embed(
        #     description= f"Test context",
        #     color= 0xABFFE4
        # )
        embed.title= 'afdsaf'
        embed.set_author(name= 'Qwerty', icon_url= 'attachment://icon.png')
        embed.set_footer(text= m)
        
        await msg.edit(embed=embed)
        
        
    
    # 放大表符
    @commands.hybrid_command(name= '放大表符', aliases=['big', 'emoji', "big_emoji", '大表符'])
    @app_commands.describe(emoji= '表情符號')
    async def big_emoji(self, ctx: commands.Context, emoji: str):
        '''
        別名 big | emoji
        放大表符
        '''
        _= emoji.split(':')[-1][:-1]
        
        url = f"https://cdn.discordapp.com/emojis/{_}.gif"
        
        # 如果不是 GIF
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    url= url[:-3]+'png'
        
        await ctx.send(url)
        
    
    # 刪除指定數量訊息
    @commands.hybrid_command(name= '刪除大量訊息', aliases= ['cls_text', 'cls', 'clst', 'clear_text'], description= '刪除指定數量訊息')
    @app_commands.describe(num= '要刪除的訊息數量')
    async def clear_text(self, ctx: commands.Context, num: int):
        '''
        +數字 : 刪除指定數量訊息
        '''
            
        await ctx.channel.purge(limit= num)
        
        embed= discord.Embed(
            description= f"成功刪除 {num} 則訊息",
            color= 0xAB8787
        )
        await ctx.send(embed= embed, ephemeral= True)

async def setup(bot):
    await bot.add_cog(Message(bot))
