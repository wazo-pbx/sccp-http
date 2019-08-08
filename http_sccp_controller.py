'''
Created on Aug 7, 2019

@author: nballas
'''

import asyncio
from fastapi import FastAPI
from sccpphone import SCCPPhone
from actors.callactor import CallActor

from threading import Timer, Thread
from twisted.internet import reactor
from multiprocessing import Process

# Thread(target=reactor.run).start()
async def run_reactor():
    reactor.run()

task = asyncio.create_task(run_reactor())



def phone_log(msg):
    print(msg)

phone = None
sccp_controller = FastAPI()

@sccp_controller.get("/")
def read_root():
    return {"Hello": "World"}


@sccp_controller.post("/dial/{extension}")
def dial(extension: int):
    phone.dial(str(extension) + '#')

@sccp_controller.post("/register/{host}/{port}/{device_name}")
def register(host: str, port: int, device_name: str):
    controller = SCCPPhoneContoller()
    phone = SCCPPhone(host, device_name)
    phone.log = phone_log
    callActor = CallActor()
    callActor.setPhone(phone)
    callActor.setTimerProvider(controller)
    callActor.setAutoAnswer(True)

    phone.setTimerProvider(controller)
    phone.setDisplayHandler(controller)
    phone.setRegisteredHandler(controller)
    phone.setDateTimePicker(controller)
    phone.addCallHandler(callActor)
    phone.createClient()
    reader, writer = await asyncio.open_connection(host, port, loop=loop)
    phone.reader = reader
    phone.writer = writer



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
def register():
    return {"Hey": "What's up?"}

@sccp_controller.delete("/stop")
def stop():
    reactor.stop()
