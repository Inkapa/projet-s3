# -*- coding: utf-8 -*-
"""
@author: Liam
"""

from typing import Any, Dict, Union

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.account_data import Account_Data
from app.schemas.account_data import Account_DataCreate, Account_DataUpdate


class CRUDAccount_Data(CRUDBase[Account_Data, Account_DataCreate, Account_DataUpdate]):
    def create_with_owner(
        self, db: Session, *, obj_in: Account_DataCreate, owner_username: str
    ) -> Account_Data:
        obj_in_data = jsonable_encoder(obj_in)
        if obj_in_data.get("gender"):
            obj_in_data["gender"] = obj_in_data["gender"].lower()
        db_obj = self.model(**obj_in_data, owner_username=owner_username)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_owner(
        self, db: Session, *, owner_username: str
    ) -> Account_Data:
        return (
            db.query(self.model)
            .filter(Account_Data.owner_username == owner_username)
            .first()
        )

    def update(
        self,
        db: Session,
        *,
        db_obj: Account_Data,
        obj_in: Union[Account_DataUpdate, Dict[str, Any]]
    ) -> Account_Data:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)
    # def get_multi_by_owner(
    #     self, db: Session, *, owner_username: str
    # ) -> List[Account_Data]:
    #     return (
    #         db.query(self.model)
    #         .filter(Account_Data.owner_username == owner_username)
    #         .offset(0)
    #         .limit(1)
    #         .all()
    #     )



account_data = CRUDAccount_Data(Account_Data)
