import asyncio
from sccpphone import SCCPPhone
from actors.callactor import CallActor
import time

class SCCPPhoneContoller:
    def __init__(self):
        self.log = phone_log

    def createTimer(self, intervalSecs, timerCallback):
        # pass
        self.keepalive_timer = Timer(intervalSecs, timerCallback)
        self.keepalive_timer.start()

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

async def register_phone(host, port, name, loop):
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

    reader, writer = await asyncio.open_connection(host, port, loop=loop)
    phone.reader = reader
    phone.writer = writer
    phone.register()
    time.sleep(0.1)
    phone.onCapabilitiesReq(None)
    print('dialing...')
    phone.dial('1000#')

    while True:
        pass



def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(register_phone('10.33.0.1', 2000, 'SEP00164697AAAA', loop))
    loop.close()




if __name__ == '__main__':
    main()
