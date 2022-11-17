# from web.crud.base import CRUDBase
# from models.account_entity import AccountEntity
# from schemas.account_entity_base import AccountEntityBase,AccountEntityCreate
# from sqlalchemy.orm import Session
# from typing import Any, Dict, Optional, Union , List

# class CRUDAccountEntity(CRUDBase[AccountEntity, AccountEntityCreate, AccountEntityBase]):
#     def get_by_username(self, db: Session, username: str) -> Optional[AccountEntity]:
#         return db.query(AccountEntity).filter(AccountEntity.username == username).one_or_none()

#     def create(self, db: Session, obj_in: AccountEntityCreate) -> AccountEntity:
#         db_obj = AccountEntity(username=obj_in.username,
#                              password_hash=auth_handler.encode_password(obj_in.password_hash),
#                              role=obj_in.role,
#                              email=obj_in.email,
#                              phone=obj_in.phone,
#                              firstname=obj_in.firstname,
#                              lastname=obj_in.lastname,
#                              organization=obj_in.organization
#                              )
#         db.add(db_obj)
#         db.commit()
#         db.refresh(db_obj)
#         return db_obj


# accountentity = CRUDAccountEntity(AccountEntity)
