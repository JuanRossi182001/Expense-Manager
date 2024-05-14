from sqlalchemy.orm import Session
from model.spent import Spent
from schemas.spentSchema import SpentSchema
from fastapi import HTTPException
from datetime import datetime


# get all spents 
def get_spents(db:Session):
    return db.query(Spent).all()


# get spent by id
def get_spents_by_id(db:Session, spent_id: int):
    return db.query(Spent).filter(Spent.id == spent_id).first()

# create spent
def create_spent(db:Session, spent: SpentSchema):
    try:
        _spent = Spent(amount = spent.amount, date = spent.date,
                       description = spent.description, spent_type = spent.spent_type,user_id = spent.user_id)
        db.add(_spent)
        db.commit()
        db.refresh(_spent)
        return _spent.as_dict()
    except: raise HTTPException(status_code=400,detail="Fail to create entity")
    
# delete spent by id 
def delete_spent(db: Session, spent_id: int):
    try:
        _spent = get_spents_by_id(db=db, spent_id= spent_id)
        db.delete(_spent)
        db.commit()
        return f"type {spent_id} successfully deleted"
    except: raise HTTPException(status_code=400,detail="Fail to delete entity")
    
    
# update type
def update_spent(db:Session, spent_id: int, spent_amount: float, spent_desc: str, spent_date: datetime, spent_type: int, user_id: int):
    try:
        _spent = get_spents_by_id(db=db, spent_id=spent_id)
        _spent.amount = spent_amount
        _spent.description = spent_desc
        _spent.date = spent_date
        _spent.spent_type = spent_type
        _spent.user_id = user_id
        db.commit()
        db.refresh(_spent)
        return _spent.as_dict()
    except: raise HTTPException(status_code=422,detail="Unprocessable entity")