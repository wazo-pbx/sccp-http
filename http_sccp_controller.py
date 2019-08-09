'''
Created on Aug 7, 2019

@author: nballas
'''

import asyncio
from fastapi import FastAPI
from asyncio_sccp import register_phone, place_call

phone = None
sccp_controller = FastAPI()

@sccp_controller.get("/")
def read_root():
    return {"Hello": "World"}


@sccp_controller.post("/dial/{extension}")
async def dial(extension: int):
    await phone.dial(str(extension) + '#')

@sccp_controller.post("/register/{host}/{port}/{device_name}")
async def register(host: str, port: int, device_name: str):
    global phone
    loop = asyncio.get_event_loop()
    all_done = asyncio.Future()
    await register_phone(all_done, host, port, device_name, loop)
    phone = await all_done




@sccp_controller.get("/events")
def all_events():
    return {"events": ["these", "are", "events", "that", "were", "received"]}

@sccp_controller.post("/hangup")
def register():
    return {"I will hangup": "What?! Why?!"}

@sccp_controller.get("/status")
def status():
    return {"status": "I am hungry"}

@sccp_controller.post("/answer")
def answer():
    return {"Hey": "What's up?"}
