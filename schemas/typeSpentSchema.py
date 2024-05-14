from typing import Optional,Generic,TypeVar
from pydantic import BaseModel, Field
from pydantic.generics import GenericModel

T = TypeVar('T')

class TypeSpentSchema(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    
    class config:
        orm_mode = True


class RequestTypeSpent(BaseModel):
    parameter: TypeSpentSchema = Field(...)


class Response(GenericModel,Generic[T]):
    code: str
    status: str
    message: str
    result: Optional[T]    
