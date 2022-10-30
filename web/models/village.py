from sqlalchemy import Column , Integer , String , Boolean ,ForeignKey
from sqlalchemy.orm import relationship
from web.db.base_class import Base , TimestampMixin

class Village(Base):
    __tablename__ = 'villages'

    id = Column(Integer , primary_key = True , index = True , autoincrement = True)
    Village = Column(String(200) , index = True , unique = True)
    provinceId = Column( Integer , ForeignKey('provinces.id') )
    district = Column( Integer , ForeignKey('districts.id') )
