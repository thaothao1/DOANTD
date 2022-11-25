from sqlalchemy import Column , Integer , String , ForeignKey
from sqlalchemy.orm import relationship
from web.db.base_class import TimestampMixin , Base

class Category( Base, TimestampMixin):
    __tablename__ = "categories"

    id = Column(Integer , primary_key= True , index = True , autoincrement= True)
    name = Column(String(1000))
