from fastapi import APIRouter, HTTPException, Depends
from service.typeSpentService import create_type,delete_type,get_type_by_id,get_types,update_type
from config.config import sessionlocal
from sqlalchemy.orm import Session
from schemas.typeSpentSchema import Response, RequestTypeSpent
from service.userService import get_current_user
from typing import Annotated

router = APIRouter()

def get_db():
    try:
        db= sessionlocal()
        yield db
    finally:
        db.close()

user_dependency = Annotated[dict,Depends(get_current_user)]        
        
# create type end point
@router.post("/Type/create")
async def create(user: user_dependency,request: RequestTypeSpent, db: Session = Depends((get_db))):
    try:
        if user is None:
            raise HTTPException(status_code=401,
                                detail="Authentication failed")
        create_type(db=db,typee=request.parameter)
        return Response(code="200", status="OK",message="Type created Successfully", result=None).dict(exclude_none=True)
    except:
        raise HTTPException(status_code=500,detail="Fail to create data")
    
    
# get all types end point
@router.get("/Type")
async def get_all(user: user_dependency,db:Session = Depends((get_db))):
    try:
        if user is None:
            raise HTTPException(status_code=401,
                                detail="Authentication failed")
        _types = get_types(db=db)
        return Response(code="200", status="OK",message="Succes fetch all data", result=_types).dict(exclude_none=True)
    except:
        raise HTTPException(status_code=400,detail="Fail to get data")
    
    
# get type by id end point
@router.get("/Type/{type_id}")
async def get_by_id(user: user_dependency,type_id: int, db: Session = Depends((get_db))):
    try:
        if user is None:
            raise HTTPException(status_code=401,
                                detail="Authentication failed")
        _type = get_type_by_id(db=db,type_id=type_id)
        return Response(code="200", status="OK",message="Succes fetch all data", result=_type).dict(exclude_none=True)
    except:
        raise HTTPException(status_code=400,detail="Fail to get data")
    
    
# update type end point
@router.patch("/Type/update/{type_Id}")
async def update(user: user_dependency,type_id: int, request: RequestTypeSpent, db: Session = Depends((get_db))):
    try:
        if user is None:
            raise HTTPException(status_code=401,
                                detail="Authentication failed")
        _type = update_type(db=db, type_id=type_id,type_desc=request.parameter.description,type_name=request.parameter.name)
        return Response(code="200", status="OK",message="Type updated successfully", result=_type).dict(exclude_none=True)
    except:
        raise HTTPException(status_code=422,detail="Fail to update data")

    
# delete type end point   
@router.delete("/Type/delete/{type_id}")
async def delete(user: user_dependency,type_id: int, db: Session = Depends((get_db))):
    try:
        if user is None:
            raise HTTPException(status_code=401,
                                detail="Authentication failed")
        delete_type(db=db,type_id=type_id)
        return Response(code="200", status="OK",message="Type deleted successfully", result=None).dict(exclude_none=True)
    except:
        raise HTTPException(status_code=404, detail="Fail to delete data, data not found")