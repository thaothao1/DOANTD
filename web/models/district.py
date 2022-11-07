from sqlalchemy import Column , Integer , String , Boolean ,ForeignKey
from sqlalchemy.orm import relationship
from db.base_class import Base , TimestampMixin

class District(Base ,  TimestampMixin):
    __tablename__ = "districts"

    id = Column(Integer , primary_key = True , index = True , autoincrement = True)
    district = Column(String(200) , index = True , unique = True)
    provinceId = Column(Integer , ForeignKey("provinces.id"))
