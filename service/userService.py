from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from model.user import User
from datetime import timedelta,datetime,date
from typing import Annotated
from fastapi import Depends,HTTPException
from jose import jwt,JWTError
from starlette import status
from schemas.userSchema import UserSchema
from sqlalchemy.orm.exc import NoResultFound





        
SECRET_KEY = '55e8b7ae3ffbfa4d8d34d00b3c213944'
ALGORITH = 'HS256'
bycrypt_context = CryptContext(schemes=['bcrypt'], deprecated ='auto')
oauth_bearer = OAuth2PasswordBearer(tokenUrl='/token')


# get users
def get_users(db: Session):
    return db.query(User).all()
    
    
# get user by id 
def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()
    
    
# get super users
def get_super_users(db: Session):
    return db.query(User).filter(User.isSuper_user == True).all()
    
    
# get normal users
def get_noraml_user(db: Session):
    return db.query(User).filter(User.isSuper_user == False).all()



# create user
def create_user(db: Session, user: UserSchema):
    try:
        mail_name_already_exist(db=db, user=user) # REVISAR PORQUE ME DA SOLO EL ERROR 500 Y NO LOS OTROS QUE ESTAN EN LA FUNCION
        
        _user = User(
            username=user.username,
            password=bycrypt_context.hash(user.password),
            isSuper_user=user.isSuper_user,
            birth_date=user.birth_date,
            email=user.email
     )
        db.add(_user)
        db.commit()
        db.refresh(_user)
        return _user.as_dict()
    except HTTPException as e:
        raise e
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Fail to create user")


# delete user by id 
def delete_by_id(user_id: int, db: Session):
    try:
        _user = get_user_by_id(user_id=user_id,db=db)
        db.delete(_user)
        db.commit()
        return f"User {user_id} successfully deleted"
    except NoResultFound:
        raise HTTPException(status_code=404,detail="Error, user not found")
    
    
# update user
def update_user(user_id: int, username: str, password: str, isSuper_user: bool, email: str, birth_date: date, db: Session):
    try:
        _user = get_user_by_id(user_id=user_id,db=db)
        _user.username = username
        _user.password = bycrypt_context.hash(password)
        _user.isSuper_user = isSuper_user
        _user.email = email
        _user.birth_date = birth_date
        db.commit()
        db.refresh(_user)
        return _user.as_dict()
    except:
        raise HTTPException(status_code=422,detail="Unprocessable entity")
      
      
# authenticate user 
def authenticate_user(user: UserSchema, db: Session):
    _user = db.query(User).filter(User.username == user.username).first()
    if not _user:
        raise HTTPException(status_code=404,detail="Error, incorrect username")
    if not bycrypt_context.verify(user.password,_user.password):
        raise HTTPException(status_code=404,detail="Error, incorrect password")
    if not _user.isSuper_user == user.isSuper_user:
        raise HTTPException(status_code=404, detail="Error, incorrect role")
    return _user


# authenticate user for token
def authenticate_user_2(username: str, password: str, db: Session):
    _user = db.query(User).filter(User.username == username).first()
    if not _user:
        return False
    if not bycrypt_context.verify(password, _user.password):
        return False
    return _user


# create token 
def create_access_token(username: str, user_id: int, expires_delta: timedelta):
     encode = {'sub': username,'id': user_id}
     expires = datetime.utcnow() + expires_delta
     encode.update({'exp':expires})
     return jwt.encode(encode,SECRET_KEY,algorithm=ALGORITH)
    
    
# get current user 
async def get_current_user(token: Annotated[str,Depends(oauth_bearer)]):
    try:
        payload = jwt.decode(token,SECRET_KEY)
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        IsSuper_user: bool = payload.get('role')
        birth_date: date = payload.get('birth_date')
        email: str = payload.get('email')
        if username is None or user_id is None or IsSuper_user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                    detail="Could not validate user.")
        return {'username': username, 'id': user_id,'role': IsSuper_user,'birth_date': birth_date, 'email': email}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="could not validate user")

def mail_name_already_exist(db: Session, user: UserSchema):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    existing_email = db.query(User).filter(User.email == user.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already exists")
    
    