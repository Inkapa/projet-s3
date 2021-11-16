# -*- coding: utf-8 -*-
"""
Created on Wed Oct 6 00:15:27 2021

@author: Liam
"""

from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import constr
from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/me", response_model=schemas.Account_Data)
def read_account_data_me(
    db: Session = Depends(deps.get_db),
    current_account: models.Account = Depends(deps.get_current_active_account),
) -> Any:
    """
    Retrieve own data.
    """

    data = crud.account_data.get_by_owner(
        db=db, owner_username=current_account.username
    )
    return data


@router.put("/me", response_model=schemas.Account_Data)
def update_data_me(
    *,
    db: Session = Depends(deps.get_db),
    data_in: schemas.Account_DataUpdate,
    current_account: models.Account = Depends(deps.get_current_active_account),
) -> Any:
    """
    Update own data.
    """
    data = crud.account_data.get_by_owner(
        db=db, owner_username=current_account.username
    )
    if not data:
        raise HTTPException(status_code=404, detail="Data not found")
    if data.owner_username != current_account.username:
        raise HTTPException(status_code=500, detail="Mismatch between current user's username and linked data's owner")
    data = crud.account_data.update(db=db, db_obj=data, obj_in=data_in)
    return data


@router.get("/{username}", response_model=schemas.Account_Data)
def read_data_by_username(
    *,
    db: Session = Depends(deps.get_db),
    username: constr(strip_whitespace=True, min_length=4, max_length=40),
    current_account: models.Account = Depends(deps.get_current_active_account),
) -> Any:
    """
    Get data by username.
    """
    account = crud.account.get_by_username(db=db, username=username)
    if not account:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system",
        )
    data = crud.account_data.get_by_owner(db=db, owner_username=account.username)
    if not data:
        raise HTTPException(status_code=404, detail="Data not found")
    return data


@router.post("/{username}", response_model=schemas.Account_Data)
def create_account_data_by_username(
    *,
    db: Session = Depends(deps.get_db),
    username: constr(strip_whitespace=True, min_length=4, max_length=40),
    data_in: schemas.Account_DataCreate,
    current_account: models.Account = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new data (for testing purposes, should always be created on register).
    """
    account = crud.account.get_by_username(db=db, username=username)
    if not account:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system",
        )
    data = crud.account_data.create_with_owner(db=db, obj_in=data_in, owner_username=account.username)
    return data


@router.put("/{username}", response_model=schemas.Account_Data)
def update_data_by_username(
    *,
    db: Session = Depends(deps.get_db),
    username: constr(strip_whitespace=True, min_length=4, max_length=40),
    data_in: schemas.Account_DataUpdate,
    current_account: models.Account = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update data by username.
    """

    account = crud.account.get_by_username(db=db, username=username)
    if not account:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system",
        )
    data = crud.account_data.get_by_owner(
        db=db, owner_username=username
    )
    if not data:
        raise HTTPException(
            status_code=404,
            detail="Data not found"
        )

    data = crud.account_data.update(db=db, db_obj=data, obj_in=data_in)
    return data
