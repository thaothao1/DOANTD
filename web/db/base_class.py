from email.policy import default
import typing as t
from sqlalchemy.ext.declarative import as_declarative , declared_attr
from sqlalchemy import Column , Integer , DateTime
from sqlalchemy.sql import  func

class_registry: t.Dict = {}
@as_declarative(class_registry = class_registry)
class Base:
    id : t.Any
    __name__ : str

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    id = Column(Integer , primary_key = True)

class TimestampMixin(object):
    created_at = Column(DateTime , default = func.now())
    changed_at = Column(DateTime , default= func.now())