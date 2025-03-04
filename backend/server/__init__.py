import asyncio, os, dotenv
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Request, Depends
from contextlib import asynccontextmanager
from .models import init_db
from .routers import api_discord, oauth, api_sounds, api_twitch
from fastapi_csrf_protect import CsrfProtect
from fastapi_csrf_protect.exceptions import CsrfProtectError
from pydantic import BaseModel

dotenv.load_dotenv()

# Lifespan 管理 FastAPI 的生命週期
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 啟動前的初始化邏輯
    print("初始化資料庫...")
    init_db()  # 初始化資料表
    await asyncio.sleep(1)
    await api_discord.init_discord_bot()
    await asyncio.sleep(5)
    # await api_twitch.init_twitch_bot()

    yield  # 等待應用啟動完成

    # 關閉時的清理邏輯
    print("關閉應用：進行清理工作...")
    # await api_twitch.close_twitch_bot()
    await api_discord.close_discord_bot()


# 創建 FastAPI 應用，並註冊 lifespan
app = FastAPI(lifespan=lifespan)

# 設定 CSRF 配置
class CsrfSettings(BaseModel):
    secret_key: str = os.getenv("CSRF_SECRET")

@CsrfProtect.load_config
def get_csrf_config():
    return CsrfSettings()

# 處理 CSRF 錯誤
@app.exception_handler(CsrfProtectError)
def csrf_error_handler(request: Request, exc: CsrfProtectError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )
    
@app.get("/csrf-token")
def get_csrf(csrf_protect: CsrfProtect = Depends()):
    # 生成簽名的 CSRF Token
    csrf_signed_token= csrf_protect.generate_csrf_tokens()
    # 設置 CSRF Token 到 Cookie
    response = JSONResponse(status_code= 200, content={"csrf_token": "cookie"})
    csrf_protect.set_csrf_cookie(csrf_signed_token, response)
    return response

@app.post("/submit-form")
def submit_form(csrf_protect: CsrfProtect = Depends()):
    # 驗證 CSRF Token
    csrf_protect.validate_csrf(csrf_protect.get_csrf_from_headers())
    return {"message": "Form submitted successfully!"}


app.include_router(router= oauth.router, prefix='/oauth')
app.include_router(router= api_discord.router, prefix='/discord')
app.include_router(router= api_sounds.router, prefix='/sounds')
app.include_router(router= api_twitch.router, prefix='/twitch')
