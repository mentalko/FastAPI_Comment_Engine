from datetime import datetime
from typing import List, Optional

from bson.objectid import ObjectId
from odmantic import Field, Model, EmbeddedModel
from pydantic import EmailStr, BaseModel

from core.db import db, engine



class Comment(Model):
    # id: int
    created_by: str 
    content: str 
    reputation: int = 0
    
    replies: List = [] 
    created_at: datetime = datetime.now()

    class Config:
        collection = 'comment'
        json_encoders = {ObjectId: str}


    @classmethod
    async def find_by_id(cls, id: str) -> Optional['Comment']:
        if not ObjectId.is_valid(id):
            return None

        return await engine.find_one(Comment, {'_id': ObjectId(id)})

    def add_reply(self, reply):
        print(reply)
        if not self.replies:
            self.replies = []
        self.replies += [reply]
        
    def add_reputation(self, count):
        self.reputation += count



class CommentCreate(BaseModel):
    name: str
    content: str
    
    
    
#      f'field "{self.name}" not yet prepared so type is still a ForwardRef, '
# pydantic.errors.ConfigError: field "replies" not yet prepared so type is still a ForwardRef, you might need to call CommentSerializer.update_forward_refs().

