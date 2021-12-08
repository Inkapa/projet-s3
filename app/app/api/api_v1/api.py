# -*- coding: utf-8 -*-
"""
Created on Thu Oct 7 00:10:54 2021

@author: Liam
"""

from fastapi import APIRouter

from app.api.api_v1.endpoints import account_data, login, account, utils, home, register, verify, misc, activity, \
    participation, athletes

# All router endpoints are gathered here
api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(account.router, prefix="/account", tags=["account"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(account_data.router, prefix="/account_data", tags=["account_data"])
api_router.include_router(home.router, tags=["home"])
api_router.include_router(register.router, prefix="/register", tags=["register"])
api_router.include_router(verify.router, prefix="/verify", tags=["verify"])
api_router.include_router(misc.router, prefix="/misc", tags=["misc"])
api_router.include_router(activity.router, prefix="/activity", tags=["activity"])
api_router.include_router(participation.router, prefix="/participation", tags=["participation"])
api_router.include_router(athletes.router, prefix="/athletes", tags=["athletes"])
