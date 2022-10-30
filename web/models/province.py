from sqlalchemy import Column , Integer , String , Boolean ,ForeignKey
from sqlalchemy.orm import relationship
from db.base_class import Base , TimestampMixin

class Province(Base):
    __tablename__ = "provinces"

    id = Column(Integer , primary_key = True , index = True , autoincrement = True)
    province = Column(String(200) , index = True , unique = True)
