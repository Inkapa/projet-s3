# -*- coding: utf-8 -*-
"""
Created on Thu Oct 7 01:56:06 2021

@author: Liam
"""

from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.core import security
from app.core.config import settings
from app.db.session import SessionLocal

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_current_account(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> models.Account:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = schemas.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    print("DATA: ", token_data.sub)
    account = crud.account.get_by_email(db, email=token_data.sub)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account


def get_current_active_account(
    current_account: models.Account = Depends(get_current_account),
) -> models.Account:
    if not crud.account.is_confirmed(current_account):
        raise HTTPException(status_code=400, detail="The account has not confirmed their email")
    return current_account


def get_current_active_superuser(
    current_account: models.Account = Depends(get_current_account),
) -> models.Account:
    if not crud.account.is_superuser(current_account):
        raise HTTPException(
            status_code=400, detail="The account doesn't have enough privileges"
        )
    return current_account
