# -*- coding: utf-8 -*-
"""
Created on Wed Oct 6 00:10:21 2021

@author: Liam
"""

from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException
from pydantic import constr
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("", response_model=List[schemas.Account])
def read_accounts(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_account: models.Account = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Retrieve accounts.
    """
    accounts = crud.account.get_multi(db, skip=skip, limit=limit)
    return accounts


@router.post("", response_model=schemas.Account)
def create_account(
    *,
    db: Session = Depends(deps.get_db),
    account_in: schemas.AccountCreate,
    current_account: models.Account = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new account.
    """
    email = crud.account.get_by_email(db, email=account_in.email)
    username = crud.account.get_by_username(db, username=account_in.username)
    if email:
        raise HTTPException(
            status_code=400,
            detail="An account with this email is already registered.",
        )
    if username:
        raise HTTPException(
            status_code=400,
            detail="An account with this username is already registered.",
        )
    account = crud.account.create(db, obj_in=account_in)
    return account


@router.put("/me", response_model=schemas.Account)
def update_account_me(
    *,
    db: Session = Depends(deps.get_db),
    account_in: schemas.AccountUpdateMe,
    current_account: models.Account = Depends(deps.get_current_active_account),
) -> Any:
    """
    Update own account.
    """
    if account_in.password is not None:
        pass
        # TODO: Send email warning password changed?
    new_account = crud.account.get_by_username(db, username=account_in.username)
    if new_account and new_account.username != current_account.username:
        raise HTTPException(
            status_code=404,
            detail="A user with the desired username already exists in the system",
        )
    account = crud.account.update(db, db_obj=current_account, obj_in=account_in)
    return account


@router.get("/me", response_model=schemas.Account)
def read_account_me(
    db: Session = Depends(deps.get_db),
    current_account: models.Account = Depends(deps.get_current_active_account),
) -> Any:
    """
    Get current account.
    """
    return current_account

@router.get("/{username}", response_model=schemas.Account)
def read_account_by_username(
    username: constr(strip_whitespace=True, min_length=4, max_length=40),
    current_account: models.Account = Depends(deps.get_current_active_account),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific account by username.
    """
    account = crud.account.get_by_username(db, username=username)
    if not account:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system",
        )
    # if account == current_account:
    #     return account
    # if not crud.account.is_superuser(current_account):
    #     raise HTTPException(
    #         status_code=400, detail="The account doesn't have enough privileges"
    #     )
    return account


@router.put("/{username}", response_model=schemas.Account)
def update_account_by_username(
    *,
    db: Session = Depends(deps.get_db),
    username: str,
    account_in: schemas.AccountUpdate,
    current_account: models.Account = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update an account by username.
    """
    account = crud.account.get_by_username(db, username=username)
    if not account:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system",
        )
    new_account = crud.account.get_by_username(db, username=account_in.username)
    if new_account and new_account.username != account.username:
        raise HTTPException(
            status_code=404,
            detail="A user with the desired username already exists in the system",
        )
    new_email = crud.account.get_by_email(db, username=account_in.email)
    if new_email and new_email.email != account.email:
        raise HTTPException(
            status_code=404,
            detail="A user with the desired email already exists in the system",
        )
    return crud.account.update(db, db_obj=account, obj_in=account_in)
