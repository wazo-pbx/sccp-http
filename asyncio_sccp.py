import asyncio
from sccpphone import SCCPPhone
from utils.timer import Timer
import time
from network.sccpprotocol import SCCPProtocol
from sccp.sccpcallstate import SCCPCallState
import logging
from sccpphone_errors import DeviceAlreadyRegistered, DeviceNotRegistered

class SCCPPhoneContoller:
    def __init__(self):
        self.log = phone_log
        self.registree = None
        self.call_duration_min = 200
        self.call_duration_max = 500
        self.auto_answer = False
        self.current_call_state = SCCPCallState.SCCP_CHANNELSTATE_ONHOOK
        self.current_call_id = 0
        self.current_line = 0
        self.phone = None

    def create_timer(self, interval_secs, timer_callback):
        self.log('creating timer')
        Timer(interval_secs, timer_callback)

    def on_registered(self):
        self.registree.registered = True

    def on_line_stat(self, message):
        pass

    def display_line_info(self, line, number):
        pass

    def set_datetime(self, day, month, year, hour, minute, seconds):
        pass

    def set_phone(self, phone):
        self.phone = phone

    def create_one_shot_timer(self, timer_in_sec, timer_handler):
        self._one_shot_timer = Timer(timer_in_sec, timer_handler, repeating=False)

    def get_auto_answer(self):
        return self.auto_answer

    def set_timer_provider(self, timer_provider):
        self.timer_provider = timer_provider

    def set_auto_answer(self, auto_answer):
        self.auto_answer = auto_answer


    def handle_call(self, line, callid, call_state):
        if not self.auto_answer:
            return
        if call_state == SCCPCallState.SCCP_CHANNELSTATE_RINGING:
                if self.current_call_id == 0:
                    self.phone.answer_call()
                    self.current_call_id = callid
                    self.current_line = line
        if call_state == SCCPCallState.SCCP_CHANNELSTATE_CONNECTED:
            pass
            # timer_in_sec = 5 #random.randrange(self.call_duration_min,self.call_duration_max)
            # self.timer_provider.create_one_shot_timer(timer_in_sec, self.on_call_end_timer)

        if call_state == SCCPCallState.SCCP_CHANNELSTATE_ONHOOK and self.current_call_id == callid:
            self.current_call_id = 0

        if call_state == SCCPCallState.SCCP_CHANNELSTATE_CALLWAITING:
            self.phone.test_complete = True

        self.current_call_state = call_state

    async def on_call_end_timer(self):
        self.log('ending call...')
        self.phone.end_call(self.current_line, self.current_call_id)
        self.log('ended call...')

    async def hangup(self):
        self.phone.end_call(self.current_line, self.current_call_id)

    async def call(self, number):
        self.phone.dial(str(number) + '#')

logger = logging.getLogger('asyncio_accp_phone')

def phone_log(msg):
    logger.info(msg)

controller = None

async def register_phone(host, port, name, loop):
    """
    Creates an SCCP phone and registers it to the given host
    """
    global controller
    if controller is not None:
        raise DeviceAlreadyRegistered(name)

    controller = SCCPPhoneContoller()
    phone = SCCPPhone(host, name)
    phone.log = phone_log

    phone.set_timer_provider(controller)
    phone.set_display_handler(controller)
    phone.set_registered_handler(controller)
    phone.set_datetime_picker(controller)
    phone.add_call_handler(controller)

    controller.set_phone(phone)
    controller.set_timer_provider(controller)
    controller.set_auto_answer(False)

    transport, protocol =  await loop.create_connection(SCCPProtocol, host, port)
    phone.ip_addr = transport.get_extra_info('sockname')[0]
    task = asyncio.create_task(phone.run(protocol))
    await task

    while not phone.registered:
        await asyncio.sleep(0.1)


async def place_call(number_to_dial):
    """
    Call a given endpoint
    """
    if not controller:
        raise DeviceNotRegistered()
    else:
        task = asyncio.create_task(controller.call(number_to_dial))
        await task

async def hangup_call():
    """
    hangup a call in progress
    """
    if controller:
        task = asyncio.create_task(controller.hangup())
        await task

async def pickup_call():
    """
    Pick up a call
    """
    if controller:
        task = asyncio.create_task(controller.phone.answer_call())
        await task
    else:
        raise DeviceNotRegistered()

async def get_received_phone_events(future):
    """
    Gte the events received by the phone
    """
    if controller:
        future.set_result(controller.phone.messages_received)
        await future
    else:
        future.set_result(None)

async def get_phone_status(future):
    """
    Get the status of the phone, i.e. is a call in progress?
    """
    if controller:
        future.set_result({"callInProgress": controller.phone.call_in_progress})
        await future
    else:
        raise DeviceNotRegistered()

async def get_phone_states(future):
    """
    Gte the status of the phone, i.e. is a call in progress?
    """
    if controller:
        future.set_result(controller.phone.states_history)
        await future
    else:
        raise DeviceNotRegistered()

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
