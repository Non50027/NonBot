from discord.ext import commands
from cryptography.fernet import Fernet
import os, bcrypt
import aiohttp

class CogCore(commands.Cog):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot= bot
        self.key_path= os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "secret.key")
    
    async def get_ctx(self):
        ch= self.bot.get_channel(656791892440121354)
        msg= await ch.fetch_message(1289805561952600126)
        ctx= await self.bot.get_context(msg)
        return ctx

    async def post_data(self, url, data= None):
        async with aiohttp.ClientSession() as session:
            header= {
                'accept': 'application/json'
            }
            async with session.post(url, headers=header, data= data) as response:
                response_data= await response.json()
                if response.status== 200:
                    return response_data
                elif response.status== 403: 
                    print("資料已經存在，無法新增！")
                    return None
                else:
                    print(f"發生錯誤，狀態碼: {response.status}")
                    print(response.text)

    async def get_data(self, url):
        async with aiohttp.ClientSession() as session:
            header= {
                'accept': 'application/json'
            }
            async with session.get(url, headers=header) as response:
                response_data= await response.json()
                if response.status== 200:
                    return response_data
                else:
                    print(f"發生錯誤，狀態碼: {response.status}")
                    print(response.text)
                    
        
    # 生成加密金鑰
    async def generate_key(self, ):
        key = Fernet.generate_key()
        with open(self.key_path, "wb") as key_file:
            key_file.write(key)

    # 載入加密金鑰
    async def load_key(self, ):
        with open(self.key_path, "rb") as key_file:
            return key_file.read()

    # 加密資料
    async def encrypt_data(self, data):
        key = await self.load_key()
        fernet = Fernet(key)
        encrypted = fernet.encrypt(data.encode('utf-8'))
        return encrypted

    # 解密資料
    async def decrypt_data(self, encrypted_data):
        key = await self.load_key()
        fernet = Fernet(key)
        decrypted = fernet.decrypt(encrypted_data).decode('utf-8')
        return decrypted

    # 將密碼加密
    async def hash_password(self, plain_password):
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(plain_password.encode('utf-8'), salt)
        return hashed

    # 驗證密碼
    async def verify_password(self, plain_password, hashed_password):
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
