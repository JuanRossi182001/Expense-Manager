from fastapi import APIRouter, HTTPException, Depends
from config.config import sessionlocal
from sqlalchemy.orm import Session
from schemas.userSchema import RequestUser,Response,RequestUserAuth
from service.userService import authenticate_user_2,get_current_user,get_noraml_user,get_super_users,get_user_by_id,get_users,delete_by_id,update_user,create_user,create_access_token,authenticate_user
from model.token import Token
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
router = APIRouter()

# PARA LOS ENDPOINT QUE QUIERA PROTEJER, OSEA QUE NECESUTE ESTAR LOGUEADO PARA UTILIZAR DEBO DARLE COMO PARAMETRO A LA FUNCION DE EL ENDPOINT UN DB: user_dependency
# user_dependency = Annotated[dict,Depends(get_current_user)]




def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()
        
# create user end point
@router.post("/User/Create")
async def create(request: RequestUser, db: Session = Depends((get_db))):
    try:
        create_user(db=db,user=request.parameter)
        return Response(code="200", status="OK",message="User created Successfully", result=None).dict(exclude_none=True)
    except:
        raise HTTPException(status_code=500,detail="Fail to create data")
    
    
# get all users end point
@router.get("/User")
async def get(db:Session = Depends(get_db)):
    _users = get_users(db=db)
    return Response(code="200", status="OK",message="succes fetch all data",result=_users).dict(exclude_none=True)


# get user by id end point
@router.get("/User/{user_id}")
async def get_by_id(user_id: int, db: Session = Depends(get_db)):
    _user = get_user_by_id(db=db,user_id=user_id)
    if not _user:
        raise HTTPException(status_code=404,detail="Fail to get data, table not found")
    return Response(code="200",status="OK",message="Succes get data",result=_user).dict(exclude_none = True)


# get super users end point
@router.get("/User/super")
async def get_super(db: Session = Depends((get_db))):
    try: 
        _superUsers = get_super_users(db=db)
        return Response(code="200",status="OK",message="Succes get data",result=_superUsers).dict(exclude_none = True)
    except:
        return HTTPException(status_code=404,detail="Fail to get data, super users not found")


# get only normal users end point
@router.get("/User/normal")
async def get_normal(db: Session = Depends((get_db))):
    try:
        _normalUsers = get_noraml_user(db=db)
        return Response(code="200",status="OK",message="Succes get data",result=_normalUsers).dict(exclude_none = True)
    except:
        return HTTPException(status_code=404,detail="Fail to get data, normal users not found")


# update user end point
@router.patch("/User/update/{user_id}")
async def update(user_id: int, request: RequestUser, db: Session = Depends(get_db)):
    _user = update_user(user_id=user_id,username=request.parameter.username,password=request.parameter.password,
                        isSuper_user=request.parameter.isSuper_user,email=request.parameter.email,
                        birth_date=request.parameter.birth_date,db=db)
    return Response(code="200",status="OK",message ="Succes update data", result =_user).dict(exclude_none = True)


# delete user end point 
@router.delete("/User/delete/{user_id}")
async def delete (user_id: int, db: Session = Depends((get_db))):
    delete_by_id(user_id=user_id,db=db)
    return Response(code="200", status="OK", message="Succes delete data", result={}).dict(exclude_none = True)


# authenticate user
@router.post("/User/auth")
async def auth(request: RequestUserAuth, db: Session = Depends((get_db))):
    try:
        _user = authenticate_user(user=request.parameter, db=db)
        if not _user:
            raise HTTPException(status_code=401,detail="fail to athenticate")
        return Response(code="200", status="OK", message="successfully authenticated", result=_user).dict(exclude_none = True)
    except:
        raise HTTPException(status_code=401,detail="Some parameter is wrong")


@router.post("/token",response_model=Token)
async def login_for_token(form_data:  Annotated[OAuth2PasswordRequestForm,Depends()],db: Session = Depends((get_db))):
    user = authenticate_user_2(form_data.username,form_data.password,db=db)
    if not user:
        raise HTTPException(status_code=401,detail="Could not validate Waiter")
    
    token = create_access_token(username=user.username,user_id=user.id,expires_delta=timedelta(minutes=10))
    
    return {'access_token': token, 'token_type': 'bearer'}

