# -*- coding: utf-8 -*-
"""
@author: Liam
"""

from typing import Any, List, Optional, Literal, Union
from pydantic import constr
from fastapi import APIRouter, Depends, Query, HTTPException, Body
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.post("/me", response_model=schemas.Participation)
def add_participation_to_me(
    *,
    db: Session = Depends(deps.get_db),
    data_in: schemas.CreateParticipationActivity,
    current_account: models.Account = Depends(deps.get_current_active_account),
) -> Any:
    """
    Add participation to activity
    """
    activity = crud.activity.get_by_id(db=db, id=data_in.activity_id)
    if not activity:
        raise HTTPException(
            status_code=404,
            detail="The activity specified wasn't found on the server",
        )

    if activity.organizer == current_account.username:
        raise HTTPException(
            status_code=422,
            detail=f"You are the creator of this activity.",
        )

    if crud.participation.get_by_user_and_id(db=db, id=data_in.activity_id, participant=current_account.username):
        raise HTTPException(
            status_code=422,
            detail="The account is already participating to this activity",
        )
    levels = [level.level for level in activity.levels]
    if data_in.level not in levels:
        raise HTTPException(
            status_code=422,
            detail=f"The activity only allows the following levels: {levels}.",
        )

    data = schemas.participation.ParticipationCreate(level=data_in.level, participant=current_account.username,
                                                     activity_id=data_in.activity_id)
    participation = crud.participation.create(db=db, obj_in=data)
    return participation


@router.get("/me", response_model=List[schemas.ParticipationActivity])
def read_participations_from_me(
    active: Optional[bool] = None,
    sport_id: Optional[int] = None,
    postcode: Optional[str] = None,
    levels: Optional[
            Union[List[Literal["débutant", "amateur", "intermédiaire", "confirmé", "expert"]], None]] = Query(None),
    offset: Optional[int] = None,
    limit: Optional[int] = None,
    db: Session = Depends(deps.get_db),
    current_account: models.Account = Depends(deps.get_current_active_account)
) -> Any:
    """
    Retrieve the user's participations
    """

    if sport_id is not None and not crud.sport.get(db=db, id=sport_id):
        raise HTTPException(
            status_code=404,
            detail="The sport specified wasn't found on the server",
        )

    data = crud.participation.get_by_user(
        db=db, participant=current_account.username, sport_id=sport_id, active=active, postcode=postcode,
        level_names=levels, offset=offset, limit=limit
    )

    return data


@router.get("/{username}", response_model=List[schemas.ParticipationActivity])
def read_participations_from_user(
    username: constr(strip_whitespace=True, min_length=4, max_length=40),
    active: Optional[bool] = None,
    sport_id: Optional[int] = None,
    postcode: Optional[str] = None,
    levels: Optional[
            Union[List[Literal["débutant", "amateur", "intermédiaire", "confirmé", "expert"]], None]] = Query(None),
    offset: Optional[int] = None,
    limit: Optional[int] = None,
    db: Session = Depends(deps.get_db),
    current_account: models.Account = Depends(deps.get_current_active_account)
) -> Any:
    """
    Retrieve the user's participations
    """

    if sport_id is not None and not crud.sport.get(db=db, id=sport_id):
        raise HTTPException(
            status_code=404,
            detail="The sport specified wasn't found on the server",
        )

    account = crud.account.get_by_username(db=db, username=username)
    if not account:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system",
        )

    data = crud.participation.get_by_user(
        db=db, participant=username, sport_id=sport_id, active=active, postcode=postcode,
        level_names=levels, offset=offset, limit=limit
    )

    return data


@router.get("/users/{id}", response_model=List[schemas.ParticipationUser])
def read_participations_to_activity(
    id: int,
    postcode: Optional[str] = None,
    roles: Optional[Union[List[Literal['0', '1', '2']], None]] = Query(None),
    levels: Optional[
            Union[List[Literal["débutant", "amateur", "intermédiaire", "confirmé", "expert"]], None]] = Query(None),
    offset: Optional[int] = None,
    limit: Optional[int] = None,
    db: Session = Depends(deps.get_db),
    current_account: models.Account = Depends(deps.get_current_active_account)
) -> Any:
    """
    Retrieve the users participating to an activity
    """

    if not crud.activity.get_by_id(db=db, id=id):
        raise HTTPException(
            status_code=404,
            detail="The activity specified wasn't found on the server",
        )

    data = crud.participation.get_by_activity(
        db=db, id=id, postcode=postcode,
        role_ids=roles, level_names=levels, offset=offset, limit=limit
    )

    return data


@router.delete("/{id}", response_model=schemas.Msg)
def delete_participation_from_me(
    id: int,
    db: Session = Depends(deps.get_db),
    current_account: models.Account = Depends(deps.get_current_active_account)
) -> Any:
    """
    Delete participation with activity id.
    """

    if not crud.participation.get_by_user_and_id(db=db, id=id, participant=current_account.username):
        raise HTTPException(
            status_code=404,
            detail=f"Could not find any matching participations from {current_account.username}",
        )

    crud.participation.remove(db=db, id=id, username=current_account.username)

    return {"msg":"participation has been successfully removed"}
