# -*- coding: utf-8 -*-
"""
@author: Liam
"""

from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException
from pydantic import constr
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/sports", response_model=List[schemas.Sport])
def get_sports(
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    Retrieve all sports
    """

    data = crud.sport.get_all(db=db)
    return data

@router.get("/sport/{name}", response_model=schemas.Sport)
def get_sport_by_name(
    db: Session = Depends(deps.get_db),
    *,
    name: constr(max_length=50, to_lower=True)
) -> Any:
    """
    Retrieve a sport by its name
    """

    data = crud.sport.get_by_name(db=db, name=name)
    return data


@router.get("/levels", response_model=List[schemas.Level])
def get_levels(
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    Retrieve all levels
    """

    data = crud.level.get_all(db=db)
    return data

@router.get("/level/{name}", response_model=schemas.Level)
def get_level_by_name(
    db: Session = Depends(deps.get_db),
    *,
    name: constr(max_length=50, to_lower=True)
) -> Any:
    """
    Retrieve a Level by its name
    """

    data = crud.level.get_by_name(db=db, name=name)
    return data