import json, discord, os, time
from typing import Literal
from tabulate import tabulate
from discord.ext import commands
from discord import app_commands
from discord_bot.tool import CogCore, MyDecorators
from datetime import datetime as dt


class Rank(CogCore):
        
    # get rank_json data
    def userList(self, guildName: str, type: str) -> list:
        
        file_path= os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "rank.json")
    
        # read rank_json
        with open(file_path, 'r', encoding= 'utf8') as file:
            data = json.load(file)
        
        # 欲處理資料
        if type== 'voice':
            for key, value in data[type][guildName].items():
                data[type][guildName][key]= f'{value[0]:3d} 天 {value[1]}'
            

        # 回傳排序後資料
        # return sorted(data.items(), key= lambda item: (item[1][0], item[1][1]), reverse= True)
        return sorted(data[type][guildName].items(), key= lambda item: item[1], reverse= True)

    # show rank
    @commands.hybrid_command(name= 'rank', description= '顯示排行榜' , aliases= ['積分'])
    @app_commands.describe(type= '要顯示的類別', select= '要顯示的範圍')
    async def rank(self, ctx: commands.Context, type: Literal['chat', 'voice'], select: Literal['all', 'top5']):
        '''
        顯示排行榜
        type: (chat 文字聊天 | voice 語音時數)
        select: (all 顯示全部 | top5 顯示前五名)
        '''
        # 設定標頭
        if type== 'chat':
            msg= '聊天'
            # header= ['名稱', '聊天次數']
        else:
            msg= '語音'
            # header= ['名稱', '語音時數']
        try:
        # 顯示全部
            if select== 'all':
                table= tabulate(self.userList(ctx.channel.guild.name, type), showindex= range(1, len(self.userList(ctx.channel.guild.name, type))+1)) 
            
            # 顯示前五名
            else:
                table= tabulate(self.userList(ctx.channel.guild.name, type)[:5], showindex= range(1, 6))
            
            # print(table)
        except Exception as e:
            table= tabulate(self.userList(ctx.channel.guild.name, type), showindex= range(1, len(self.userList(ctx.channel.guild.name, type))+1)) 
            print('rank error', e)
        await ctx.send(f'{msg}排行榜 {select}\n'+table)
    
    # 語音連接時數紀錄
    @commands.Cog.listener()
    @MyDecorators.readJson('rank')
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        
        
        
        # 進入語音
        if before.channel is None:
            # init guild data
            self.json_data.setdefault('voice', {}).setdefault(after.channel.guild.name, {}).setdefault(member.display_name, [0, "00:00:00", 0])[2]= time.time()
                
        # 離開語音
        if after.channel is None:
            
            if self.json_data['voice'][before.channel.guild.name][member.display_name][2] ==0: return
            
            # 停留的時間+ 分離出超過1天
            add_time= str(dt.now()- dt.fromtimestamp(self.json_data['voice'][before.channel.guild.name][member.display_name][2])).split(', ')
            
            # 如果超過1天就直接增加天數
            if len(add_time)== 2:
                self.json_data['voice'][before.channel.guild.name][member.display_name][0]+= int(add_time[0].split(' ')[0])
            
            # 將 停留時間 與 目前時間 做成 時 分 秒 分開的 list 用以後續計算
            add_time= [int(_) for _ in add_time[-1].split('.')[0].split(':')]
            now_time= [int(_) for _ in self.json_data['voice'][before.channel.guild.name][member.display_name][1].split(':')]
            # 用來儲存進位
            temp_time= 0
            
            # 增加時間
            for i in range(2, -1, -1):
                now_time[i]+= add_time[i]
                if i== 0:
                    temp_time= now_time[i]// 24
                    now_time[i]= now_time[i]% 24
                else:
                    temp_time= now_time[i]// 60
                    now_time[i]= now_time[i]% 60
                now_time[i-1]+= temp_time
            self.json_data['voice'][before.channel.guild.name][member.display_name][0]+= temp_time
            
            # 歸零 防止因 BOT 下線時的紀錄缺失 BUG
            self.json_data['voice'][before.channel.guild.name][member.display_name][2] =0
            
            # 存回 json 前處理
            now_time= [str(_) for _ in now_time]
            self.json_data['voice'][before.channel.guild.name][member.display_name][1]= ':'.join(now_time) 
            
        return self.json_data
        
    # 紀錄聊天次數紀錄
    @commands.Cog.listener()
    @MyDecorators.readJson('rank')
    async def on_message(self, message: discord.Message):
        # 排除 Bot 跟 指令
        if message.author.bot or message.content[0]== '|': return None
        
        self.json_data.setdefault('chat', {}).setdefault(message.guild.name, {}).setdefault(message.author.display_name, 0)
        self.json_data['chat'][message.guild.name][message.author.display_name] += 1
        
        return self.json_data
    
    @commands.Cog.listener()
    @MyDecorators.readJson('rank')
    async def on_ready(self):
        # all guild
        for guild in self.bot.discord.guilds:
            # 將已在語音頻道中的成員寫入資料ˋ
            for voiceChannel in guild.voice_channels:
                # no member
                if voiceChannel.members== []: continue
                
                # init guild data
                self.json_data.setdefault('voice', {}).setdefault(guild.name, {})
                    
                for member in voiceChannel.members:
                    # is member data
                    if member.display_name in self.json_data['voice'][guild.name]:
                        # 紀錄進入時間
                        self.json_data['voice'][guild.name][member.display_name][2] = time.time()
                        
                    # add new user
                    else:
                        # 建立初始化資料
                        self.json_data['voice'][guild.name][member.display_name]= [0, "00:00:00", time.time()]

        return self.json_data

async def setup(bot):
    await bot.add_cog(Rank(bot))
