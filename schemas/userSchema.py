from typing import Optional,Generic,TypeVar,List
from pydantic import BaseModel, Field
from pydantic.generics import GenericModel
from datetime import date
from model.spent import Spent

T = TypeVar('T')

class UserSchema(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    isSuper_user: Optional[bool] = None
    birth_date: Optional[date] = None
    email: Optional[str] = None
    
    
    class config:
        orm_mode = True
        
        
class UserSchemaAuth(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    isSuper_user: Optional[bool] = None
    
        
class RequestUserAuth(BaseModel):
    parameter: UserSchemaAuth = Field(...)
    
    
class RequestUser(BaseModel):
    parameter: UserSchema = Field(...)
    
    
class Response(GenericModel,Generic[T]):
    code: str
    status: str
    message: str
    result: Optional[T]
    
