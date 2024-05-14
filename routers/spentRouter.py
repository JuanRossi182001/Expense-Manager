from fastapi import APIRouter, HTTPException, Depends
from config.config import sessionlocal
from schemas.spentSchema import Response, RequestSpent
from sqlalchemy.orm import Session
from service.spentService import create_spent,get_spents,get_spents_by_id,delete_spent,update_spent
from service.userService import get_current_user
from typing import Annotated

router = APIRouter()

def get_db():
    try:
        db = sessionlocal()
        yield db
    finally:
        db.close()

user_dependency = Annotated[dict,Depends(get_current_user)]

# create spent end point
@router.post("/Spent/create")
async def create(user: user_dependency,request: RequestSpent, db: Session = Depends((get_db))):
    try:
        if user is None:
            raise HTTPException(status_code=401,
                                detail="Authentication failed")
            
        create_spent(db=db,spent=request.parameter)
        return Response(code="200", status="OK",message="Spent created Successfully", result=None).dict(exclude_none=True)
    except:
        raise HTTPException(status_code=500,detail="Fail to create data")
    
    
# get all spents end point
@router.get("/Spent")
async def get(user: user_dependency,db: Session = Depends((get_db))):
    try:
        if user is None:
            raise HTTPException(status_code=401,
                                detail="Authentication failed")
        _spents = get_spents(db=db)
        return Response(code="200", status="OK",message="Success fetch all data", result=_spents).dict(exclude_none=True)
    except:
        raise HTTPException(status_code=400,detail="Fail to get data")
    

# get spent by id end point
@router.get("/Spent/{spent_Id}")
async def get_by_id(user: user_dependency,spent_id: int, db: Session = Depends((get_db))):
    try:
        if user is None:
            raise HTTPException(status_code=401,
                                detail="Authentication failed")
        _spent = get_spents_by_id(db=db,spent_id=spent_id)
        return Response(code="200", status="OK",message="Success fetch all data", result=_spent).dict(exclude_none=True)
    except:
        raise HTTPException(status_code=400,detail="Fail to get data")
    
    
# update spent end point
@router.patch("/Spent/update/{spent_id}")
async def update(user: user_dependency,spent_id: int, request: RequestSpent, db: Session = Depends((get_db))):
    try:
        if user is None:
            raise HTTPException(status_code=401,
                                detail="Authentication failed")
        _spent = update_spent(db=db,spent_id=spent_id,spent_amount=request.parameter.amount,
                              spent_desc=request.parameter.description,spent_date=request.parameter.date,
                              spent_type=request.parameter.spent_type,user_id=request.parameter.user_id)
        return Response(code="200", status="OK",message="Spent updated successfully", result=_spent).dict(exclude_none=True)
    except: 
        raise HTTPException(status_code=422,detail="Fail to update data")
    
# delete spent end point
@router.delete("/Spent/delete/{spent_id}")
async def delete(user: user_dependency,spent_id: int, db: Session = Depends((get_db))):
    try:
        if user is None:
            raise HTTPException(status_code=401,
                                detail="Authentication failed")
        delete_spent(db=db,spent_id=spent_id)
        return Response(code="200", status="OK",message="Spent deleted successfully", result=None).dict(exclude_none=True)
    except:
        raise HTTPException(status_code=404, detail="Fail to delete data, data not found")
      