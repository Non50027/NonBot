from discord.ext import commands
from ..tool import CogCore


class Password(CogCore):
    
    @commands.hybrid_command()
    async def create_token(self, ctx: commands.Context):
        try:
            await self.generate_key()
        except Exception as e:
            print('create key error', e)
        await ctx.send("OK")
            
    @commands.hybrid_command()
    async def save_token(self, ctx:commands.Context, token: str):
        try:
            encrypted_token= await self.encrypt_data(token)
        except Exception as e:
            print('save token error', e)
        await ctx.send(f"token: {token}\nencrypted token: {encrypted_token}")
        
    @commands.hybrid_command()
    async def load_token(self, ctx:commands.Context, token: str):
        try:
            decrypted_token= await self.decrypt_data(token)
        except Exception as e:
            print('load token error', e)
        await ctx.send(f"encrypted token: {token}\ndecrypted token: {decrypted_token}")
        
    @commands.hybrid_command()
    async def password(self, ctx:commands.Context, password: str):
        try:
            hash_pswd= await self.hash_password(password)
        except Exception as e:
            print('hash password error', e)
        await ctx.send(f"token: {password}\nencrypted token: {hash_pswd}")
        
    @commands.hybrid_command()
    async def eq_password(self, ctx:commands.Context, password: str, hash_pswd: str):
        try:
            eq= await self.verify_password(password, hash_pswd)
            if eq:
                await ctx.send(f"OK")
            else:
                await ctx.send(f"eq password 錯誤")
        except Exception as e:
            print('eq password error', e)
        
async def setup(bot):
    await bot.add_cog(Password(bot))
    