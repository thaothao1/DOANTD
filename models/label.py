from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from web.db.base_class import Base, TimestampMixin

class Label(Base , TimestampMixin):
    __tablename__ = "labels"

    id = Column(Integer , primary_key = True , index = True , autoincrement = True)
    name = Column(String(200))

