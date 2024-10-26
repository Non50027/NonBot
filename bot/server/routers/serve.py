
from fastapi import APIRouter

router= APIRouter(prefix='/option')

@router.get('/')
async def home():
    return {'bot': 'outline'}
