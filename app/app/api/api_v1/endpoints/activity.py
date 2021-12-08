# -*- coding: utf-8 -*-
"""
@author: Liam
"""

from typing import Any, List, Optional, Literal, Union
from pydantic import constr
from fastapi import APIRouter, Depends, Query, HTTPException, Body
from sqlalchemy.orm import Session
import datetime
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
    Create new activity for current user
    """

    if not crud.sport.get(db=db, id=data_in.sport_id):
        raise HTTPException(
            status_code=404,
            detail="The sport specified wasn't found on the server",
        )
    if data_in.event_date < datetime.date.today():
        raise HTTPException(
            status_code=422,
            detail="The event's date cannot be prior to today",
        )
    activity = crud.activity.create_with_organizer(db=db, obj_in=data_in, organizer=current_account.username)
    return activity


@router.put("/me", response_model=schemas.Activity)
def update_activity_me(
    *,
    activity_id: int = Body(..., embed=True),
    db: Session = Depends(deps.get_db),
    data_in: schemas.ActivityUpdate,
    current_account: models.Account = Depends(deps.get_current_active_account),
) -> Any:
    """
    Update an activity for current user
    """
    activity = crud.activity.get(db=db, id=activity_id)
    if not activity:
        raise HTTPException(
            status_code=404,
            detail="The activity wasn't found on the server",
        )

    if activity.organizer != current_account.username:
        raise HTTPException(
            status_code=422,
            detail="You cannot edit other people's activities",
        )
    if data_in.sport_id is not None and not crud.sport.get(db=db, id=data_in.sport_id):
        raise HTTPException(
            status_code=404,
            detail="The sport specified wasn't found on the server",
        )

    if data_in.event_date and data_in.event_date < datetime.date.today():
        raise HTTPException(
            status_code=422,
            detail="The event's date cannot be prior to today",
        )
    activity = crud.activity.update(db=db, db_obj=activity, obj_in=data_in)
    return activity


@router.get("/me", response_model=List[schemas.Activity])
def read_activities_me(
    active: Optional[bool] = None,
    sport_id: Optional[int] = None,
    postcode: Optional[str] = None,
    offset: Optional[int] = None,
    limit: Optional[int] = None,
    levels: Optional[
            Union[List[Literal["débutant", "amateur", "intermédiaire", "confirmé", "expert"]], None]] = Query(None),
    db: Session = Depends(deps.get_db),
    current_account: models.Account = Depends(deps.get_current_active_account)
) -> Any:
    """
    Retrieve activities created by the current user.
    """

    if sport_id is not None and not crud.sport.get(db=db, id=sport_id):
        raise HTTPException(
            status_code=404,
            detail="The sport specified wasn't found on the server",
        )

    data = crud.activity.get_with_queries(
        db=db, organizer=current_account.username, sport_id=sport_id, active=active, postcode=postcode, levels=levels,
        offset=offset, limit=limit
    )
    return data


@router.get("/{id}", response_model=schemas.ActivityWithParticipants)
def read_activity_with_id(
    id: int,
    db: Session = Depends(deps.get_db),
    current_account: models.Account = Depends(deps.get_current_active_account)
) -> Any:
    """
    Retrieve activity with its id.
    """

    data = crud.activity.get_by_id(
        db=db, id=id
    )
    if not data:
        raise HTTPException(
            status_code=404,
            detail="The specified activity was not found on the server",
        )
    return data


@router.delete("/{id}", response_model=schemas.Activity)
def delete_activity_with_id(
    id: int,
    db: Session = Depends(deps.get_db),
    current_account: models.Account = Depends(deps.get_current_active_account)
) -> Any:
    """
    Delete activity with its id.
    """

    data = crud.activity.get_by_id(
        db=db, id=id
    )
    if not data:
        raise HTTPException(
            status_code=404,
            detail="The specified activity was not found on the server",
        )
    if data.organizer != current_account.username:
        raise HTTPException(
            status_code=422,
            detail="You cannot delete other people's activities",
        )
    crud.participation.remove(db=db, id=id)
    data = crud.activity.remove(
        db=db, id=id
    )

    return data


@router.get("", response_model=List[schemas.Activity])
def read_activities(
    active: Optional[bool] = None,
    sport_id: Optional[int] = None,
    postcode: Optional[str] = None,
    exclude_participating: Optional[bool] = None,
    me_excluded: Optional[bool] = None,
    offset: Optional[int] = None,
    limit: Optional[int] = None,
    levels: Optional[
            Union[List[Literal["débutant", "amateur", "intermédiaire", "confirmé", "expert"]], None]] = Query(None),
    db: Session = Depends(deps.get_db),
    current_account: models.Account = Depends(deps.get_current_active_account)
) -> Any:
    """
    Retrieve activities.
    """

    data = crud.activity.get_with_queries(
        db=db, current_account=current_account.username,
        sport_id=sport_id, active=active, postcode=postcode, exclude_participating=exclude_participating,
        me_excluded=me_excluded, levels=levels, offset=offset, limit=limit
    )
    return data

@router.get("/user/{username}", response_model=List[schemas.Activity])
def read_activities(
    username: constr(strip_whitespace=True, min_length=4, max_length=40),
    active: Optional[bool] = None,
    sport_id: Optional[int] = None,
    postcode: Optional[str] = None,
    offset: Optional[int] = None,
    limit: Optional[int] = None,
    levels: Optional[
            Union[List[Literal["débutant", "amateur", "intermédiaire", "confirmé", "expert"]], None]] = Query(None),
    db: Session = Depends(deps.get_db),
    current_account: models.Account = Depends(deps.get_current_active_account)
) -> Any:
    """
    Retrieve activities created by the username.
    """

    data = crud.activity.get_with_queries(
        db=db, organizer=username,
        sport_id=sport_id, active=active, postcode=postcode,
        levels=levels, offset=offset, limit=limit
    )
    return data

