from sqlalchemy import Column,String,Boolean,Date,Integer
from config.config import base



class User(base):
    
    __tablename__ = "Users"
    
    id = Column(Integer,primary_key=True)
    username = Column(String)
    password = Column(String)
    isSuper_user = Column(Boolean)
    birth_date = Column(Date)
    email = Column(String)
    
    
    def as_dict(self):
        return{
            'id': self.id,
            'username': self.username,
            'password': self.password,
            'IsSuper_user': self.isSuper_user,
            'birth_date': self.birth_date,
            'email': self.email
        }