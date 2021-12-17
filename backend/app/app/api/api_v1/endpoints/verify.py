# -*- coding: utf-8 -*-
"""
Created on Mon Oct 11 22:03:51 2021

@author: Liam
"""

from typing import Any
from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.api import deps
from app.core.security import get_password_hash
from app.utils import verify_verification_token
from app.core.config import settings
from app.utils import (
    generate_verification_token,
    send_new_account_email,
    check_email,
)
router = APIRouter()


@router.post("/password", response_model=schemas.Msg)
def reset_password(
    reset_info: schemas.Reset_Password,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Reset password
    """
    email = verify_verification_token(reset_info.token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid token")
    account = crud.account.get_by_email(db, email=email)
    if not account:
        raise HTTPException(
            status_code=404,
            detail="The account with this username does not exist in the system.",
        )
    elif not crud.account.is_confirmed(account):
        raise HTTPException(status_code=400, detail="The account has not confirmed their email")
    hashed_password = get_password_hash(reset_info.new_password)
    account.hashed_password = hashed_password
    db.add(account)
    db.commit()
    return {"msg": "Password updated successfully"}


@router.post("/resend-email", response_model=schemas.Msg)
def resend_email(
    db: Session = Depends(deps.get_db),
    login: str = Body(..., embed=True),
) -> Any:
    """
    Resend verification email
    """
    if check_email(login):
        account = crud.account.get_by_email(db, email=login)
    else:
        account = crud.account.get_by_username(db, username=login)

    if account and crud.account.is_confirmed(account):
        raise HTTPException(
            status_code=400,
            detail="The account has already been confirmed.",
        )

    elif account and settings.EMAILS_ENABLED:

        account_token = generate_verification_token(email=account.email)
        send_new_account_email(
            email_to=account.email, username=account.username, token=account_token
        )
    else:
        raise HTTPException(
            status_code=400,
            detail="The account does not exist or email verification has been disabled.",
        )
    return {"msg":"Verification email successfully resent"}


@router.get("/account", response_model=schemas.Msg)
def verify_email(
    token: str,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Verify email
    """
    email = verify_verification_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid token")
    account = crud.account.get_by_email(db, email=email)
    if not account:
        raise HTTPException(
            status_code=404,
            detail="The account with this email does not exist in the system.",
        )
    if crud.account.is_confirmed(account):
        raise HTTPException(
            status_code=400,
            detail="The account has already been confirmed.",
        )
    account.is_confirmed = True
    db.add(account)
    db.commit()
    return {"msg": "Account verified successfully"}