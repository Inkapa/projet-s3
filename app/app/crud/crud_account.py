# -*- coding: utf-8 -*-
"""
@author: Liam
"""

from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models.account import Account
from app.schemas.account import AccountCreate, AccountUpdate
from app.utils import check_email

class CRUDAccount(CRUDBase[Account, AccountCreate, AccountUpdate]):

    def get_by_email(self, db: Session, *, email: str) -> Optional[Account]:
        return db.query(Account).filter(func.lower(Account.email) == email.lower()).first()

    def get_by_username(self, db: Session, *, username: str) -> Optional[Account]:
        return db.query(Account).filter(func.lower(Account.username) == username.lower()).first()

    def create(self, db: Session, *, obj_in: AccountCreate) -> Account:
        db_obj = Account(
            username=obj_in.username,
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            is_superuser=obj_in.is_superuser,
            is_confirmed=obj_in.is_confirmed,
            role_id=obj_in.role_id,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: Account, obj_in: Union[AccountUpdate, Dict[str, Any]]
    ) -> Account:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data.get("password"):
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(self, db: Session, *, login: str, password: str) -> Optional[Account]:
        if check_email(login):  # Check if account is an email or a username
            account = self.get_by_email(db, email=login)
        else:
            account = self.get_by_username(db, username=login)
        if not account:
            return None
        if not verify_password(password, account.hashed_password):
            return None
        return account

    def is_superuser(self, account: Account) -> bool:
        return account.is_superuser

    def is_confirmed(self, account: Account) -> bool:
        return account.is_confirmed


account = CRUDAccount(Account)
