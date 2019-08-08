import asyncio
from sccpphone import SCCPPhone
from actors.callactor import CallActor
from utils.timer import Timer
import time
from network.sccpprotocol import SCCPProtocol

class SCCPPhoneContoller:
    def __init__(self):
        self.log = phone_log

    def createTimer(self, intervalSecs, timerCallback):
        print('creating timer')
        self.keepalive_timer = Timer(intervalSecs, timerCallback)

    def onRegistered(self):
        self.log('Registered...')

    def onLineStat(self, message):
        pass

    def displayLineInfo(self, line, number):
        pass

    def setDateTime(self, day,month,year,hour,minute,seconds):
        pass

    def createOneShotTimer(self, timerInSec, timerHandler):
        pass

def phone_log(msg):
    print(msg)

async def run_phone(host, port, name, loop):
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
    on_con_lost = loop.create_future()
    message = 'Hello World!'
    transport, protocol =  await loop.create_connection(SCCPProtocol, host, port)
    # protocol.client = phone
    task = asyncio.create_task(phone.run(protocol))
    # loop.run_until_complete(task)
    # phone.dial('1000#')

    try:
        await on_con_lost
    finally:
        transport.close()



def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_phone('10.33.0.1', 2000, 'SEP00164697AAAA', loop))
    loop.close()




if __name__ == '__main__':
    main()
