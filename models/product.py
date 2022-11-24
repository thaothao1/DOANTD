from itertools import product
from sqlalchemy import Column , Integer , String , ForeignKey
from sqlalchemy.orm import relationship
from web.db.base_class import TimestampMixin , Base

class Product( Base , TimestampMixin):
    __tablename__ = "products"

    id = Column(Integer , primary_key = True , index = True , autoincrement = True)
    name = Column(String(1150))
    link = Column(String(2150))
    image = Column(String(5000))
    price =Column(String(1150))
    priceSale = Column(String(1150))
    rating = Column(String(1000))
    shopId = Column(Integer() , ForeignKey("shops.id"))
    labelId = Column(Integer() , ForeignKey("labels.id"), nullable= True)
    categoryId = Column(Integer() , ForeignKey("categories.id"), nullable= True)


