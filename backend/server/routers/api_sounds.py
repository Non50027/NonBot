import os, uuid
from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlmodel import Session, select
from ..models import get_session, Sound, SoundCreate, SoundOutput#, Tag, SoundOutputWithTags, TagOutputWithSounds, TagOutput

router= APIRouter()


@router.post('/{sound_name}', response_model= SoundOutput)
async def upload_sound(sound_name: str, file: UploadFile, session: Session= Depends(get_session), description: str= None):
    
    sound_id= str(uuid.uuid4())[5:17]
    file_name= f"{sound_name}-{sound_id}.{file.filename.split('.')[-1]}"
    # file_path= os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + '\\static\\sounds\\' + file_name
    file_path= os.path.dirname(__file__).split('\\backend')[0] + '\\static\\sounds\\' + file_name
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
    
    sound= Sound(
        id=sound_id,
        name= sound_name,
        file_name= file_name,
    )
    
    session.add(sound)
    session.commit()
    return sound

@router.get('/all', response_model= list[SoundOutput])
async def get_all(session: Session= Depends(get_session)):
    all_data= session.exec(select(Sound)).all()
    return all_data

@router.delete('/{sound_id}', response_model= SoundOutput)
async def delete_sound(sound_id: str, session: Session= Depends(get_session)):
    sound= session.get(Sound, sound_id)
    if not sound:
        raise HTTPException(status_code=404, detail="Sound not found")
    session.delete(sound)
    session.commit()
    return sound

# @router.post('/tag/{tag_name}', response_model= TagOutput)
# async def create_tag(tag: str, session: Session= Depends(get_session)):
#     tag= Tag.model_validate(tag)
#     session.add(tag)
#     session.commit()
#     session.refresh(tag)
#     return tag

# @router.post('/upload', response_model= SoundOutputWithTags)
# async def upload_sound(sound: SoundCreate, tag_ids: list[int], file: UploadFile, session: Session= Depends(get_session), description: str= None):
    
#     sound_dict= sound.model_dump()
    
#     # 處理 sound
#     sound_id= str(uuid.uuid4())[5:17]
#     file_name= f"/{sound.name}-{sound_id}.{file.filename.split('.')[-1]}"
#     file_path= os.path.join(os.path.dirname(__file__).split('\\bot')[0], 'static', 'sounds', file_name)
#     with open(file_path, "wb") as buffer:
#         buffer.write(await file.read())
    
#     # 處理 tag
#     tags= [session.get(Tag, id) for id in tag_ids]
    
#     sound_dict.update({
#         'id': sound_id,
#         'file_name': file_name,
#         'tags': tags
#     })
    
#     sound= Sound( **sound_dict)
#     session.add(sound)
#     session.commit()
#     session.refresh(sound)
#     return sound