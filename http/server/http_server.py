from fastapi import FastAPI

sccp = FastAPI()

@sccp.get("/")
def read_root():
    return {"Hello": "World"}


@sccp.post("/dial/{extension}")
def dial(item_id: int):
    return {"extension": 1000}

@sccp.post("/register/{host}/{port}/{device_name}")
def register(host: str, port: int, device_name: str):
    return {"host": "10.0.0.1", port: 5001, device_name: "SOME_MAC_ADDRESS"}

@sccp.get("/events")
def all_events():
    return {"events": ["these", "are", "events", "that", "were", "received"]}

@sccp.post("/hangup")
def register():
    return {"I will hangup": "What?! Why?!"}

@sccp.get("/status")
def status():
    return {"status": "I am hungry"}

@sccp.post("/answer")
def register():
    return {"Hey": "What's up?"}
