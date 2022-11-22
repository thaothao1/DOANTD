from sqlalchemy import Column , Integer , String 
from web.db.base_class import Base , TimestampMixin

class Shop(Base ,TimestampMixin):
    __tablename__ = "shops"

    id = Column(Integer , primary_key = True , index = True , autoincrement = True)
    name = Column(String(200))
    link = Column(String(200))
