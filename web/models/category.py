from sqlalchemy import Column , Integer , String , Boolean ,ForeignKey
from sqlalchemy.orm import relationship
from web.db.base_class import Base , TimestampMixin

class Category(Base , TimestampMixin):
    __tablename__ = "categories"

    id = Column(Integer , primary_key = True , index = True , autoincrement = True)
    category = Column(String(200) , index = True , unique = True)
    link = Column(String(200) , nullable = False , unique = True , index = True)
    shopId = Column(Integer , ForeignKey("shops.id"))