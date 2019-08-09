import asyncio
from sccpphone import SCCPPhone
from utils.timer import Timer
import time
from network.sccpprotocol import SCCPProtocol
from sccp.sccpcallstate import SCCPCallState

class SCCPPhoneContoller:
    def __init__(self):
        self.log = phone_log
        self.registree = None
        self.callDurationMin = 200
        self.callDurationMax = 500
        self.autoAnswer = False
        self.currentCallState = SCCPCallState.SCCP_CHANNELSTATE_ONHOOK
        self.currentCallId = 0
        self.currentLine = 0

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

    def setPhone(self,phone):
        self.phone = phone

    def createOneShotTimer(self, timerInSec, timerHandler):
        pass

    def getAutoAnswer(self):
        return self.autoAnswer

    def setTimerProvider(self,timerProvider):
        self.timerProvider = timerProvider

    def setAutoAnswer(self,autoAnswer):
        self.autoAnswer = autoAnswer


    def handleCall(self,line,callid,callState):
        if not self.autoAnswer:
            return
        if callState == SCCPCallState.SCCP_CHANNELSTATE_RINGING:
                if self.currentCallId == 0:
                    self.phone.answer_call()
                    self.currentCallId = callid
                    self.currentLine = line
        if callState == SCCPCallState.SCCP_CHANNELSTATE_CONNECTED:
            timerInSec = 1#random.randrange(self.callDurationMin,self.callDurationMax)
            self.timerProvider.createOneShotTimer(timerInSec,self.onCallEndTimer)

        if callState == SCCPCallState.SCCP_CHANNELSTATE_ONHOOK and self.currentCallId == callid:
            self.currentCallId = 0

        if callState == SCCPCallState.SCCP_CHANNELSTATE_CALLWAITING:
            self.phone.test_complete = True

        self.currentCallState = callState

    def onCallEndTimer(self):
        self.phone.end_call(self.currentLine,self.currentCallId)

    async def hangup(self):
        self.phone.end_call(self.currentLine,self.currentCallId)



def phone_log(msg):
    print(time.time(), msg)
controller = None
async def register_phone(future, host, port, name, loop):
    """
    Creates an SCCP phone and registers it to the given host
    """
    global controller
    controller = SCCPPhoneContoller()
    phone = SCCPPhone(host, name)
    phone.log = phone_log

    phone.setTimerProvider(controller)
    phone.setDisplayHandler(controller)
    phone.setRegisteredHandler(controller)
    phone.setDateTimePicker(controller)
    phone.addCallHandler(controller)

    controller.setPhone(phone)
    controller.setTimerProvider(controller)
    controller.setAutoAnswer(True)

    transport, protocol =  await loop.create_connection(SCCPProtocol, host, port)
    task = asyncio.create_task(phone.run(protocol))
    await task

    while not phone.registered:
        await asyncio.sleep(0.1)

    future.set_result(phone)


async def place_call(phone, number_to_dial, loop):
    """
    Call a given endpoint
    """
    task = asyncio.create_task(phone.dial(number_to_dial))
    await task

async def hangup_call():
    """
    hangup a call in progress
    """
    task = asyncio.create_task(controller.hangup())
    await task

async def pickup_call():
    """
    Call a given endpoint
    """
    task = asyncio.create_task(controller.phone.answer_call())
    await task

async def get_received_phone_events(future):
    """
    Gte the events received by the phone
    """
    future.set_result(controller.phone.messages_received)
    await future

async def get_phone_status(future):
    """
    Gte the status of the phone, i.e. is a call in progress?
    """
    future.set_result(controller.phone.call_in_progress)
    await future

async def get_phone_states(future):
    """
    Gte the status of the phone, i.e. is a call in progress?
    """
    future.set_result(controller.phone.states_history)
    await future

async def main(loop):
    """
    Example usage
    """
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
