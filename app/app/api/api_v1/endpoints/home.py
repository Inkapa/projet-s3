# -*- coding: utf-8 -*-
"""
Created on Tue Oct 12 00:35:27 2021

@author: Liam
"""
from fastapi import APIRouter
import time
router = APIRouter()

@router.get("/")
def home_get():
    return {"status":"Online", "time":int(time.time())}

@router.post("/")
def home_post():
    return {"status":"Online", "time":int(time.time())}