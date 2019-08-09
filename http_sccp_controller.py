'''
Created on Aug 7, 2019

@author: nballas
@about: REST interface to the asyncio_sccp phone
to run: uvicorn http_sccp_controller:sccp_controller --reload
'''

import asyncio
from fastapi import FastAPI
from asyncio_sccp import register_phone, place_call, hangup_call
from asyncio_sccp import get_received_phone_events, get_phone_status, get_phone_states
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
async def all_events():
    events = asyncio.Future()
    await get_received_phone_events(events)
    states = asyncio.Future()
    await get_phone_states(states)
    return {"events": events.result(), "callStates": states.result()}

@sccp_controller.post("/hangup")
async def hangup():
    await hangup_call()

@sccp_controller.get("/status")
async def status():
    status = asyncio.Future()
    await get_phone_status(status)
    return {"callInProgress": status.result()}

@sccp_controller.post("/answer")
async def answer():
    return {"Hey": "What's up?"}
