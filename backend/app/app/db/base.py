# -*- coding: utf-8 -*-
"""
@author: Liam
"""

# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # noqa
from app.models.account_data import Account_Data  # noqa
from app.models.account import Account  # noqa
from app.models.role import Role  # noqa
from app.models.offer import Offer # noqa
from app.models.activity import Activity # noqa
from app.models.coaching import Coaching # noqa
from app.models.level import Level # noqa
from app.models.message import Message # noqa
from app.models.review import Review # noqa
from app.models.sport import Sport # noqa
from app.models.wear import Wear # noqa