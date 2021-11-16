# -*- coding: utf-8 -*-
"""
Created on Tue Oct 12 00:39:17 2021

@author: Liam
"""
from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic.networks import EmailStr
from pydantic import constr
from app import crud, schemas
from app.api import deps
from app.core.config import settings
from app.utils import (
    generate_verification_token,
    send_new_account_email,
)

router = APIRouter()


@router.post("", response_model=schemas.Account)
def register(
    *,
    db: Session = Depends(deps.get_db),
    account_in: schemas.AccountRegister,
    data_in: schemas.Account_DataCreate,
) -> Any:
    """
    Create new user without the need to be logged in.
    """
    if not settings.USERS_OPEN_REGISTRATION:
        raise HTTPException(
            status_code=403,
            detail="Open user registration is currently forbidden on this server",
        )
    get_email = crud.account.get_by_email(db, email=account_in.email)
    get_username = crud.account.get_by_username(db, username=account_in.username)
    if get_email:
        raise HTTPException(
            status_code=400,
            detail="An account with this email is already registered.",
        )
    if get_username:
        raise HTTPException(
            status_code=400,
            detail="An account with this username is already registered.",
        )
    account_in = schemas.AccountCreate(
        username=account_in.username,
        password=account_in.password,
        email=account_in.email
    )
    account = crud.account.create(db, obj_in=account_in)
    crud.account_data.create_with_owner(db=db, obj_in=data_in, owner_username=account.username)
    if settings.EMAILS_ENABLED and account_in.email:
        account_token = generate_verification_token(email=account_in.email)
        send_new_account_email(
            email_to=account_in.email, username=account_in.username, token=account_token
        )
    return account
