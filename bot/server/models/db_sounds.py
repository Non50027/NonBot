from sqlmodel import SQLModel, Field, Relationship, ForeignKey
from datetime import datetime

# class SoundTagLink(SQLModel, table=True):
#     sound_id: str = Field(foreign_key="sound.id", primary_key=True)
#     tag_id: int = Field(foreign_key="tag.id", primary_key=True)
    
class SoundBase(SQLModel):
    name: str
    description: str | None = None
    
class Sound(SoundBase, table= True):
    id: str = Field(primary_key= True)
    created_at: datetime = Field(default_factory= datetime.now)
    file_name: str

    # tags: list['Tag']| None = Relationship(back_populates= 'sounds', link_model=SoundTagLink)
    
class SoundCreate(SoundBase):
    ...
    
class SoundOutput(SoundBase):
    id: str
    file_name: str
    created_at: datetime
    name: str
    
# class SoundOutputWithTags(SoundOutput):
#     tags: list['TagOutput']
    
# class TagBase(SQLModel):
#     name: str
    
# class Tag(TagBase, table= True):
#     id: int | None = Field(default= None, primary_key= True)

#     sounds: list[Sound] | None = Relationship(back_populates= 'tags', link_model=SoundTagLink)
    
# class TagOutput(TagBase):
#     id: int
    
# class TagOutputWithSounds(TagOutput):
#     sounds: list[SoundOutput]
