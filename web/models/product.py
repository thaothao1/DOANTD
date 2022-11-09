from itertools import product
from sqlalchemy import Column , Integer , String , ForeignKey
from sqlalchemy.orm import relationship
from db.base_class import TimestampMixin , Base

class Product( Base , TimestampMixin):
    __tablename__ = "products"

    id = Column(Integer , primary_key = True , index = True , autoincrement = True)
    product = Column(String(1150))
    link = Column(String(2150))
    image = Column(String(5000))
    price =Column(String(1150))
    priceSale = Column(String(1150))
    color  = Column(String(1150))
    size = Column( String(1150) )
    description = Column(String(1150))
    quantity = Column(Integer)



    