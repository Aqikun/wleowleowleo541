# backend/src/domains/collaboration/schemas.py
from pydantic import BaseModel, ConfigDict
from datetime import datetime

class UserSchemaForMessage(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    username: str

class ChatMessageBase(BaseModel):
    content: str

class ChatMessageCreate(ChatMessageBase):
    pass

class ChatMessageInDB(ChatMessageBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    timestamp: datetime
    room_name: str
    sender: UserSchemaForMessage