# -*- coding: utf-8 -*-
"""
@author: Liam
"""

from typing import Any, List

from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from pydantic import constr
from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.post("/me", response_model=schemas.Activity)
def create_activity_me(
    *,
    db: Session = Depends(deps.get_db),
    data_in: schemas.ActivityCreate,
    current_account: models.Account = Depends(deps.get_current_active_account),
) -> Any:
    """
    Create new data activity
    """

    activity = crud.activity.create_with_organizer(db=db, obj_in=data_in, organizer=current_account.username)
    return activity


@router.get("/me", response_model=List[schemas.Activity])
def read_account_data_me(
    active: bool,
    db: Session = Depends(deps.get_db),
    current_account: models.Account = Depends(deps.get_current_active_account)
) -> Any:
    """
    Retrieve own data.
    """

    data = crud.activity.get_by_organizer(
        db=db, organizer=current_account.username, active=active
    )
    return data
