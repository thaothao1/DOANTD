from sqlalchemy import Column , Integer , String 
from web.db.base_class import Base , TimestampMixin

class Shop(Base ,TimestampMixin):
    __tablename__ = "shops"

    id = Column(Integer , primary_key = True , index = True , autoincrement = True)
    shop = Column(String(200) , index = True , unique = True)
    link = Column(String(200) , nullable = False , unique = True , index = True)