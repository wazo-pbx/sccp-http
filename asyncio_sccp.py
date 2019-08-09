import asyncio
from sccpphone import SCCPPhone
from actors.callactor import CallActor
from utils.timer import Timer
import time
from network.sccpprotocol import SCCPProtocol

class SCCPPhoneContoller:
    def __init__(self):
        self.log = phone_log
        self.registree = None

    def createTimer(self, intervalSecs, timerCallback):
        self.log('creating timer')
        self.keepalive_timer = Timer(intervalSecs, timerCallback)

    def onRegistered(self):
        self.registree.registered = True

    def onLineStat(self, message):
        pass

    def displayLineInfo(self, line, number):
        pass

    def setDateTime(self, day,month,year,hour,minute,seconds):
        pass

    def createOneShotTimer(self, timerInSec, timerHandler):
        pass

def phone_log(msg):
    print(time.time(), msg)

async def register_phone(future, host, port, name, loop):

    controller = SCCPPhoneContoller()
    callActor = CallActor()
    phone = SCCPPhone(host, name)
    phone.log = phone_log

    phone.setTimerProvider(controller)
    phone.setDisplayHandler(controller)
    phone.setRegisteredHandler(controller)
    phone.setDateTimePicker(controller)
    phone.addCallHandler(callActor)

    callActor.setPhone(phone)
    callActor.setTimerProvider(controller)
    callActor.setAutoAnswer(True)

    transport, protocol =  await loop.create_connection(SCCPProtocol, host, port)
    task = asyncio.create_task(phone.run(protocol))
    await task


    while not phone.registered:
        await asyncio.sleep(0.1)

    future.set_result(phone)


async def place_call(phone, number_to_dial, loop):
    # global phone
    task = asyncio.create_task(phone.dial(number_to_dial))
    await task

async def main(loop):
    all_done = asyncio.Future()
    await register_phone(all_done, '10.33.0.1', 2000, 'SEP00164697AAAA', loop)
    phone = await all_done
    await place_call(phone, '1000#', loop)
    while not phone.call_in_progress:
        await asyncio.sleep(0.1)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main(loop))
    finally:
        pass
