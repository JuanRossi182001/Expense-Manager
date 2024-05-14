from config.config import base
from sqlalchemy import String, Column,Integer

class TypeSpent(base):
    
    __tablename__ = "typespents"
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    
    def as_dict(self):
        return {
            'name': self.name,
            'description': self.description
        }