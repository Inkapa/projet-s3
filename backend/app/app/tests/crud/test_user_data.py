# -*- coding: utf-8 -*-
"""
@author: Liam
"""

from sqlalchemy.orm import Session

from app import crud
from app.schemas.user_data import User_DataCreate, User_DataUpdate
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string


def test_create_user_data(db: Session) -> None:
    title = random_lower_string()
    description = random_lower_string()
    data_in = User_DataCreate(title=title, description=description)
    user = create_random_user(db)
    data = crud.user_data.create_with_owner(db=db, obj_in=data_in, owner_username=user.username)
    assert data.title == title
    assert data.description == description
    assert data.owner_username == user.username


def test_get_user_data(db: Session) -> None:
    title = random_lower_string()
    description = random_lower_string()
    data_in = User_DataCreate(title=title, description=description)
    user = create_random_user(db)
    data = crud.user_data.create_with_owner(db=db, obj_in=data_in, owner_username=user.username)
    stored_data = crud.user_data.get(db=db, id=data.id)
    assert stored_data
    assert data.id == stored_data.id
    assert data.title == stored_data.title
    assert data.description == stored_data.description
    assert data.owner_username == stored_data.owner_username


def test_update_user_data(db: Session) -> None:
    title = random_lower_string()
    description = random_lower_string()
    data_in = User_DataCreate(title=title, description=description)
    user = create_random_user(db)
    data = crud.user_data.create_with_owner(db=db, obj_in=data_in, owner_username=user.username)
    description2 = random_lower_string()
    data_update = User_DataUpdate(description=description2)
    data2 = crud.user_data.update(db=db, db_obj=data, obj_in=data_update)
    assert data.id == data2.id
    assert data.title == data2.title
    assert data2.description == description2
    assert data.owner_username == data2.owner_username


def test_delete_user_data(db: Session) -> None:
    title = random_lower_string()
    description = random_lower_string()
    data_in = User_DataCreate(title=title, description=description)
    user = create_random_user(db)
    data = crud.user_data.create_with_owner(db=db, obj_in=data_in, owner_username=user.username)
    data2 = crud.user_data.remove(db=db, id=data.id)
    data3 = crud.user_data.get(db=db, id=data.id)
    assert data3 is None
    assert data2.id == data.id
    assert data2.title == title
    assert data2.description == description
    assert data2.owner_username == user.username
