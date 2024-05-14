from sqlalchemy.orm import Session
from model.typeSpent import TypeSpent
from schemas.typeSpentSchema import TypeSpentSchema
from fastapi import HTTPException



# get all types
def get_types(db: Session):
    return db.query(TypeSpent).all()

# get type by id 
def get_type_by_id(db:Session, type_id: int):
    try:
        return db.query(TypeSpent).filter(TypeSpent.id == type_id).first()
    except: raise HTTPException(status_code=404, detail="Fail type not found")

# create a new type 
def create_type(db: Session, typee: TypeSpentSchema):
    try:
        _type = TypeSpent(name=typee.name,description=typee.description)
        db.add(_type)
        db.commit()
        db.refresh(_type)
        return _type.as_dict()
    except Exception as e: raise print(e)

# delete type by id
def delete_type(db: Session, type_id: int):
    try:
        _type = get_type_by_id(db=db,type_id=type_id)
        db.delete(_type)
        db.commit()
        return f"type {type_id} successfully deleted"
    except: raise HTTPException(status_code=400,detail="Fail to delete entity")
    
    
    
# update type
def update_type(db:Session, type_id: int, type_name: str, type_desc: str):
    try:
        _type = get_type_by_id(db=db,type_id=type_id)
        _type.name = type_name
        _type.description = type_desc
        db.commit()
        db.refresh(_type)
        return _type.as_dict()
    except: raise HTTPException(status_code=422,detail="Unprocessable entity")