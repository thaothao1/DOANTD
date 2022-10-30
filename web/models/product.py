from cgi import print_exception
from itertools import product
from sqlalchemy import Column , Integer , String , ForeignKey
from sqlalchemy.orm import relationship
from web.db.base_class import TimestampMixin , Base


class Product( Base , TimestampMixin):
    __tablename__ = "products"

    id = Column(Integer , primary_key = True , index = True , autoincrement = True)
    product = Column(String(200) , index = True , unique = True)
    link = Column(String(200) , nullable = False , unique = True , index = True)
    image = Column(String(250))
    price =Column(String(250))
    priceSale = Column(String(250))
    color  = Column(String(250))
    size = Column( String(250) )
    description = Column(String(1150))
    quantity = Column(Integer)
    id_district = Column(Integer , ForeignKey("districts.id") )
    labelId = Column(Integer , ForeignKey("labels.id") )


    