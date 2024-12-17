import discord, requests, os
from discord.ext import commands, tasks
from discord import app_commands
from discord_bot.tool import CogCore


class Role(CogCore):
    
    def __init__(self, bot):
        super().__init__(bot)
        self.temp_data= None
        self.bot.loop.create_task(self._init_start_task())
    
        
    def start_task(self, fun_name):
        if fun_name.is_running():
            fun_name.restart()
        else:
            fun_name.start()
    
    async def _init_start_task(self):
        self.start_task(self.get_all_role_to_emoji)
    
    # set 回應訊息領取身份組
    @commands.hybrid_command(description= '回應訊息領取身分組')
    @app_commands.describe(message_id= '指定的訊息ID', emoji_id= '指定的反應ID', role_id= '指定的身份組')
    async def set_role_meg(self, ctx: commands.Context, message_id: str, emoji_id: str, role_id: str):
        '''
        別名: ['srm', 'set_role_meg']
        可以對回應訊息領取身份組進行設定
        message_id: 訊息ID
        emoji_id: 反應ID
        role_id: 身份組
        '''
        data={
            'guild': ctx.guild.id,
            'role': int(role_id),
            'message': int(message_id),
            'emoji': int(emoji_id)
        }
        response = requests.post(
            f"{os.getenv('VITE_BACKEND_DJANGO_URL')}/discord/set_role_message_emoji/",
            json= data
        )
        response_data= response.json()
        guild= self.bot.get_guild(response_data['guild'])
        emoji= guild.get_emoji(response_data['emoji'])
        role= guild.get_role(response_data['role'])
        for channel in guild.text_channels:
            try:
                # 嘗試取得訊息
                message= await channel.fetch_message(int(response_data['message']))
                await ctx.send(f"成功在 {message.jump_url} 設定回覆 {emoji} 取得 {role.mention}")
                return
            except discord.NotFound:
                # 如果找不到訊息，跳過
                continue
            except discord.Forbidden:
                # 如果無法存取該頻道，跳過
                continue
            except Exception as e:
                print('error', e)
            
    
    @tasks.loop(hours=6)
    async def get_all_role_to_emoji(self):
        response = requests.get(f"{os.getenv('VITE_BACKEND_DJANGO_URL')}/discord/get_role_message_emoji/")
        self.temp_data= response.json()
        
    # 回應訊息領取身份組
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        
        for data in self.temp_data:
            
            # 比對伺服器、訊息、表符
            if payload.guild_id!= data['guild']\
            or payload.message_id!= data['message']\
            or payload.emoji.id!= data['emoji']: continue
            
            guild= self.bot.get_guild(data['guild'])
            role= guild.get_role(data['role'])
            
            await payload.member.add_roles(role)
            return
        
    # 移除回應訊息移除身份組
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        for data in self.temp_data:
            
            # 比對伺服器、訊息、表符
            if payload.guild_id!= data['guild']\
            or payload.message_id!= data['message']\
            or payload.emoji.id!= data['emoji']: continue

            guild= self.bot.get_guild(data['guild'])
            role= guild.get_role(data['role'])

            await payload.member.remove_roles(role)
            return

async def setup(bot):
    await bot.add_cog(Role(bot))
