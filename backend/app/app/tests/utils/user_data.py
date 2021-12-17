# -*- coding: utf-8 -*-
"""
@author: Liam
"""

from typing import Optional

from sqlalchemy.orm import Session

from app import crud, models
from app.schemas.user_data import User_DataCreate
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string


def create_random_user_data(db: Session, *, owner_username: Optional[int] = None) -> models.User_Data:
    if owner_username is None:
        user = create_random_user(db)
        owner_username = user.username
    title = random_lower_string()
    description = random_lower_string()
    data_in = User_DataCreate(title=title, description=description, id=id)
    return crud.user_data.create_with_owner(db=db, obj_in=data_in, owner_username=owner_username)
