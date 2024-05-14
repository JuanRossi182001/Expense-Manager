from typing import Optional,Generic,TypeVar
from pydantic import BaseModel, Field
from pydantic.generics import GenericModel
from datetime import datetime

T = TypeVar('T')

class SpentSchema(BaseModel):
    amount: Optional[float] = None
    date: Optional[datetime] = None
    description: Optional[str] = None
    spent_type: Optional[int] = None
    user_id: Optional[int] = None
    
    class config:
        orm_mode = True
        
class RequestSpent(BaseModel):
    parameter: SpentSchema = Field(...)
    
    
class Response(GenericModel,Generic[T]):
    code: str
    status: str
    message: str
    result: Optional[T]