# -*- coding: utf-8 -*-
"""
@author: Liam
"""

from typing import Any, List, Optional, Literal, Union
from pydantic import confloat, constr
from fastapi import APIRouter, Depends, Query, HTTPException, Body
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.api import deps
import httpx
from lxml import html

router = APIRouter()


@router.get("/me", response_model=List[schemas.AthletesBase])
async def get_athletes(
        radius: Optional[confloat(ge=1.0, le=320)] = 10.0,
        me_excluded: Optional[bool] = None,
        postal_code: Optional[int] = None,
        sport_ids: Optional[List[int]] = Query(None),
        levels: Optional[
            Union[List[Literal["débutant", "amateur", "intermédiaire", "confirmé", "expert"]], None]] = Query(None),
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        db: Session = Depends(deps.get_db),
        current_account: models.Account = Depends(deps.get_current_active_account)
) -> Any:
    """
    Get curated list of athletes
    """
    if not postal_code:
        postal_code = crud.account_data.get_by_owner(db=db, owner_username=current_account.username).postcode

    postcodes = {postal_code}
    async with httpx.AsyncClient() as client:
        geo_response = await client.get(
            f"https://nominatim.openstreetmap.org/search?q={postal_code}&format=jsonv2&countrycodes=fr&addressdetails=1"
        )
        geo_data = geo_response.json()

        if geo_data:
            lat = geo_data[0]["lat"]
            lon = geo_data[0]["lon"]
            headers = {
                'Host': 'www.freemaptools.com',
                'Accept': 'application/xml, text/xml, */*; q=0.01',
                'User-Agent': 'Mozilla/5.0(Windows NT 10.0;Win64;x64;rv: 94.0) Gecko/20100101 Firefox/94.0',
                'Accept-Encoding': 'gzip',
                'Referer': 'https://www.freemaptools.com/find-french-postcodes-inside-radius.htm',
                'Connection': 'keep-alive',
                'DNT': '1',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'no-cors',
                'Sec-Fetch-Site': 'same-origin',
                'Pragma': 'no-cache',
                'Cache-Control': 'no-cache'
            }
            postcode_response = await client.get(
                f"https://www.freemaptools.com/ajax/fr/get-all-french-postcodes-inside.php?radius={radius}&lat={lat}&lng={lon}",
                headers=headers
            )
            post_data = postcode_response.text
            if post_data:
                root = html.fromstring(post_data)
                postcodes.update(set(root.xpath("//*[@postcode]/@postcode")))
        else:
            raise HTTPException(
                status_code=404,
                detail="The submitted postal code was not recognized.",
            )
    if sport_ids and (max(sport_ids) > 116 or min(sport_ids) < 1):
        raise HTTPException(
            status_code=404,
            detail="One or multiple of the sports specified weren't found on the server",
        )

    data = crud.participation.get_athletes(db=db, current_account=current_account.username,
                                           postcodes=list(postcodes), me_excluded=me_excluded,
                                           sport_ids=sport_ids,
                                           level_names=levels, offset=offset, limit=limit)
    users = []
    for participation in data:
        obj = next(filter(lambda user: user['account'].owner_username == participation.user.username, users), None)
        if not obj:
            obj = {'account': participation.user.data, 'sports': []}
            users.append(obj)
        obj['sports'].append({'sport': participation.activity.sport, 'level': participation.level})

    return users


@router.get("/{usersame}", response_model=List[schemas.Account_Data])
async def get_athletes_by_username(
        username: constr(strip_whitespace=True),
        me_excluded: Optional[bool] = None,
        postal_code: Optional[int] = None,
        sport_ids: Optional[List[int]] = Query(None),
        levels: Optional[
            Union[List[Literal["débutant", "amateur", "intermédiaire", "confirmé", "expert"]], None]] = Query(None),
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        db: Session = Depends(deps.get_db),
        current_account: models.Account = Depends(deps.get_current_active_account)
) -> Any:
    """
    Get list of athletes by username hint
    """
    if sport_ids and (max(sport_ids) > 116 or min(sport_ids) < 1):
        raise HTTPException(
            status_code=404,
            detail="One or multiple of the sports specified weren't found on the server",
        )
    data = crud.account_data.get_athletes_by_name(db=db, current_account=current_account.username,
                                                  username=username, me_excluded=me_excluded,
                                                  postcode=postal_code, sport_ids=sport_ids,
                                                  level_names=levels, offset=offset, limit=limit)
    return data
