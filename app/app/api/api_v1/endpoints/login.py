# -*- coding: utf-8 -*-
"""
Created on Fri Oct 8 01:06:43 2021

@author: Liam
"""

from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import EmailStr
from app import crud, models, schemas
from app.api import deps
from app.core import security
from app.core.config import settings
from app.utils import (
    generate_verification_token,
    send_reset_password_email,
)

router = APIRouter()


@router.post("/login/access-token", response_model=schemas.Token)
def login_access_token(
    db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    account = crud.account.authenticate(
        db, login=form_data.username, password=form_data.password
    )
    if not account:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not crud.account.is_confirmed(account):
        raise HTTPException(status_code=400, detail="The account has not confirmed their email")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            account.email, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@router.post("/login/test-token", response_model=schemas.Account)
def test_token(current_account: models.Account = Depends(deps.get_current_account)) -> Any:
    """
    Test access token
    """
    return current_account


@router.post("/password-recovery", response_model=schemas.Msg)
def recover_password(email: EmailStr = Body(..., embed=True), db: Session = Depends(deps.get_db)) -> Any:
    """
    Password Recovery
    """
    account = crud.account.get_by_email(db, email=email)

    if not account:
        raise HTTPException(
            status_code=404,
            detail="The account with this username does not exist in the system.",
        )
    password_reset_token = generate_verification_token(email=email)
    send_reset_password_email(
        email_to=account.email, username=account.username, token=password_reset_token
    )
    return {"msg": "Password recovery email sent"}

