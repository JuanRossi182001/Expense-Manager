from sqlalchemy import Column,String,Date,Integer,Float,ForeignKey
from config.config import base



class Spent(base):
    __tablename__ = "spents"
    
    id = Column(Integer,primary_key=True)
    amount = Column(Float)
    date = Column(Date)
    description = Column(String)
    spent_type = Column(Integer, ForeignKey("typespents.id"))
    user_id = Column(Integer,ForeignKey("Users.id"))
   
    
    def as_dict(self):
        return{
            'amount': self.amount,
            'date': self.date,
            'description': self.description,
            'spent_type': self.spent_type,
            'user_id': self.user_id
        }