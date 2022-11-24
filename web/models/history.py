from sqlalchemy import Column , Integer , String , ForeignKey
from sqlalchemy.orm import relationship
from web.db.base_class import TimestampMixin , Base

class History(Base , TimestampMixin):
    __tabelname__ = "histories"

    id = Column(Integer, primary_key=True, index = True  , autoincrement= True)
    productId = Column(Integer() , ForeignKey("products.id"), nullable= True)
    view = Column(Integer())
    



