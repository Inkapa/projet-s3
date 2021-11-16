# -*- coding: utf-8 -*-
"""
@author: Liam
"""

from sqlalchemy.orm import Session
import datetime
from app import crud, schemas
from app.core.config import settings
from app.db import base  # noqa: F401
from app.db.session import engine
base.Base.metadata.create_all(bind=engine)
def init_db(db: Session) -> None:
    # Tables should be created with Alembic migrations

    account = crud.account.get_by_email(db, email=settings.FIRST_SUPERUSER)
    if not account:
        account_in = schemas.AccountCreate(
            username="admin",
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
            is_confirmed=True,
            role_id=2,
        )
        account = crud.account.create(db, obj_in=account_in)  # noqa: F841

    account_data = crud.account_data.get_by_owner(db=db, owner_username=account.username)
    if not account_data:
        account_data_in = schemas.Account_DataCreate(
            first_name="Freeze",
            last_name="Corleone",
            postcode="93200",
            profile_picture="https://i1.sndcdn.com/artworks-ePT6bVti7OlSwvL8-zyz8cA-t500x500.jpg",
            birthday=datetime.date(day=6, month=6, year=1992),
            about="Administrateur de TPMS",
            gender='m',  # Homme
        )
        account_data = crud.account_data.create_with_owner(db, obj_in=account_data_in, owner_username=account.username)