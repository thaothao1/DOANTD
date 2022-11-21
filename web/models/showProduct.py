from sqlalchemy import Column , Integer , String  , ForeignKey
from db.base_class import Base , TimestampMixin

class ShowProduct(Base ,TimestampMixin):
    __tablename__ = "showProducts"

    id = Column(Integer , primary_key = True , index = True , autoincrement = True)
    name = Column(String(200) , unique = True )
    price = Column(String(200))
    thegioididongId = Column(Integer() , ForeignKey("products.id") , nullable= True)
    lazadaId = Column(Integer() , ForeignKey("products.id") , nullable= True)
    fptId = Column(Integer() , ForeignKey("products.id") , nullable= True)
    shopeeId = Column(Integer() , ForeignKey("products.id") , nullable= True) 
    labelId = Column(Integer() , ForeignKey("labels.id"), nullable= True) 