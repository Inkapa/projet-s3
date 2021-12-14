# -*- coding: utf-8 -*-
"""
@author: Liam
"""

from typing import Any, List
from pydantic import constr
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.api import deps
import httpx
from lxml import html

router = APIRouter()


@router.post("/me", response_model=List[schemas.AthletesBase])
async def get_athletes(
        data_in: schemas.FilterAthletesRadius,
        db: Session = Depends(deps.get_db),
        current_account: models.Account = Depends(deps.get_current_active_account)
) -> Any:
    """
    Get curated list of athletes
    """
    postal_code = data_in.postal_code
    if not postal_code:
        postal_code = crud.account_data.get_by_owner(db=db, owner_username=current_account.username).postcode

    postcodes = {postal_code}
    async with httpx.AsyncClient(timeout=40.0) as client:
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
                f"https://www.freemaptools.com/ajax/fr/get-all-french-postcodes-inside.php?radius={data_in.radius}&lat={lat}&lng={lon}",
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
    if data_in.sport_ids and (max(data_in.sport_ids) > 116 or min(data_in.sport_ids) < 1):
        raise HTTPException(
            status_code=404,
            detail="One or multiple of the sports specified weren't found on the server",
        )

    data = crud.participation.get_athletes(
        db=db, current_account=current_account.username,
        postcodes=list(postcodes), me_excluded=data_in.me_excluded,
                                           sport_ids=data_in.sport_ids,
                                           level_names=data_in.levels, offset=data_in.offset, limit=data_in.limit)
    users = []
    for participation in data:
        obj = next(filter(lambda user: user['account'].owner_username == participation.user.username, users), None)
        if not obj:
            obj = {'account': participation.user.data, 'sports': []}
            users.append(obj)
        obj['sports'].append({'sport': participation.activity.sport, 'level': participation.level})

    return users


@router.post("/{username}", response_model=List[schemas.Account_Data])
async def get_athletes_by_username(
        username: constr(strip_whitespace=True),
        data_in: schemas.FilterAthletes,
        db: Session = Depends(deps.get_db),
        current_account: models.Account = Depends(deps.get_current_active_account)
) -> Any:
    """
    Get list of athletes by username hint
    """
    if data_in.sport_ids and (max(data_in.sport_ids) > 116 or min(data_in.sport_ids) < 1):
        raise HTTPException(
            status_code=404,
            detail="One or multiple of the sports specified weren't found on the server",
        )
    data = crud.account_data.get_athletes_by_name(
        db=db, current_account=current_account.username,
        username=username, me_excluded=data_in.me_excluded,
        postcode=data_in.postal_code, sport_ids=data_in.sport_ids,
        level_names=data_in.levels, offset=data_in.offset, limit=data_in.limit
        )
    return data
