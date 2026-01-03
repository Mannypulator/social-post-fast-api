from pydantic import BaseModel, EmailStr, Field
from fastapi_users import schemas
import uuid

class CreatePost(BaseModel):
    title:str
    content:str
    
class CreateUser(schemas.BaseUserCreate):
    pass

class GetUser(schemas.BaseUser):
    pass

class UpdateUser(schemas.BaseUserUpdate):
    pass
    