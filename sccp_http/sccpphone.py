'''
Created on Jun 20, 2011

@author: lebleu1
'''
from .sccp.sccpmessagetype import SCCPMessageType
from .sccp.sccpregister import SCCPRegister
from .sccp.sccpcapabilities import SCCPCapabilitiesRes
from .sccp.sccpbuttontemplatereq import SCCPButtonTemplateReq
from .sccp.sccpregisteravailablelines import SCCPRegisterAvailableLines
from .sccp.sccptimedatereq import SCCPTimeDateReq
from .sccp.sccpcallstate import SCCPCallState
from .sccp.sccpkeypadbutton import SCCPKeyPadButton
from .sccp.sccpsoftkeyevent import SCCPSoftKeyEvent
from .sccp.sccpmessage import SCCPMessage
from .sccp.sccplinestatreq import SCCPLineStatReq
from .sccp.sccpopenreceivechannelack import SCCPOpenReceiveChannelAck
from .sccp.sccpclosereceivechannel import SCCPCloseReceiveChannel
from .network.ip_address import IpAddress
import struct

SKINNY_LBL_EMPTY = 0
SKINNY_LBL_REDIAL = 1
SKINNY_LBL_NEWCALL = 2
SKINNY_LBL_HOLD = 3
SKINNY_LBL_TRANSFER = 4
SKINNY_LBL_CFWDALL = 5
SKINNY_LBL_CFWDBUSY = 6
SKINNY_LBL_CFWDNOANSWER = 7
SKINNY_LBL_BACKSPACE = 8
SKINNY_LBL_ENDCALL = 9
SKINNY_LBL_RESUME = 10
SKINNY_LBL_ANSWER = 11

class SCCPPhone():
    '''
    Main sccp phone class
    '''


    def __init__(self, host, device_name):
        self.host = host
        self.device_name = device_name
        self.call_handler = set()
        self.registered = False
        self.call_in_progress = False
        self.ringing = False
        self.call_waiting = False
        self.messages_received = []
        self.states_history = []
        self._ip_addr = ''

    def set_logger(self, logger):
        self.log = logger

    @property
    def ip_addr(self):
        return self._ip_addr

    @ip_addr.setter
    def ip_addr(self, value):
        if isinstance(value, str):
            self._ip_addr = IpAddress(value)
        else:
            self._ip_addr = value

    async def run(self, protocol):
        self.complete_construction(protocol)
        protocol.client_ready(self)

    def set_timer_provider(self, timer_provider):
        self.timer_provider = timer_provider

    def set_registered_handler(self, registered_handler):
        self.registeredHandler = registered_handler
        self.registeredHandler.registree = self

    def set_datetime_picker(self, datetime_picker):
        self.datetime_picker = datetime_picker

    def set_display_handler(self,displayHandler):
        self.displayHandler = displayHandler

    def add_call_handler(self,callHandler):
        self.log(self.device_name + ' adding call handler')
        self.call_handler.add(callHandler)

    def complete_construction(self, protocol):
        self.log('completing construction')
        self.protocol = protocol
        self.protocol.handle_unknown_message(self.on_unknown_message)
        self.protocol.add_handler(SCCPMessageType.RegisterAckMessage,self.on_registered_ack)
        self.protocol.add_handler(SCCPMessageType.CapabilitiesReqMessage,self.on_capabilities_req)
        self.protocol.add_handler(SCCPMessageType.KeepAliveAckMessage,self.on_keep_alive_ack)
        self.protocol.add_handler(SCCPMessageType.DefineTimeDate,self.on_define_timedate)
        self.protocol.add_handler(SCCPMessageType.SetSpeakerModeMessage,self.on_set_speaker_mode)
        self.protocol.add_handler(SCCPMessageType.CallStateMessage,self.on_call_state)
        self.protocol.add_handler(SCCPMessageType.ActivateCallPlaneMessage,self.on_activate_call_plane)
        self.protocol.add_handler(SCCPMessageType.StartToneMessage,self.on_start_tone)
        self.protocol.add_handler(SCCPMessageType.LineStatMessage,self.on_line_stat)
        self.protocol.add_handler(SCCPMessageType.RegisterRejectMessage,self.on_register_reject_message)
        self.protocol.add_handler(SCCPMessageType.SetRingerMessage,self.on_set_ringer_message)
        self.protocol.add_handler(SCCPMessageType.Reset,self.on_reset_message)
        self.protocol.add_handler(SCCPMessageType.OpenReceiveChannel,self.on_open_receive_channel)
        self.protocol.add_handler(SCCPMessageType.CloseReceiveChannel,self.on_close_receive_channel)

    def register(self):
        self.log('registering device: ' + self.device_name)
        register_message = SCCPRegister(self.device_name, self.host)
        self.protocol.send_sccp_message(register_message)

    def on_open_receive_channel(self, msg):
        self.log('openning channel')
        print(msg.compression_type)
        ack = SCCPOpenReceiveChannelAck()
        ack.ip_addr = self.ip_addr
        self.protocol.send_sccp_message(ack)
        self.current_call_id = msg.conference_id

    def on_close_receive_channel(self, msg):
        self.log('closing channel')
        # print(hex(msg.conference_id), hex(msg.party_id), hex(msg.conference_id_1))

    def on_sccp_connect_success(self):
        # reason is a twisted.python.failure.Failure  object
        self.register()

    def on_sccp_connect_fail(self, reason):
        # reason is a twisted.python.failure.Failure  object
        self.log('Connection failed: %s' % reason.getErrorMessage())

    def on_register_reject_message(self, message):
        self.log('register failed ' + message.to_str())

    def on_set_ringer_message(self, message):
        self.log('ringer mode: ' + message.to_str())

    def on_reset_message(self, message):
        self.log('got reset')

    async def on_keep_alive_timer(self):
        self.log('on keep alive')
        message = SCCPMessage(SCCPMessageType.KeepAliveMessage)
        self.protocol.send_sccp_message(message)

    def on_unknown_message(self, message):
        self.log('receive unkown message ' + message.to_str())
        self.messages_received.append(message.to_str())

    def on_registered_ack(self, register_ack):
        self.log("sccp phone registered")
        self.log("--          keep_alive_interval : " + str(register_ack.keep_alive_interval))
        self.log("--               date_template : " + str(register_ack.date_template))
        self.log("-- secondarykeep_alive_interval : " + str(register_ack.secondarykeep_alive_interval))
        self.timer_provider.create_timer(register_ack.keep_alive_interval, self.on_keep_alive_timer)
        self.registeredHandler.on_registered()
        self.messages_received.append(register_ack.to_str())


    def on_keep_alive_ack(self, message):
        self.log("Keepalive ack")

    def on_capabilities_req(self, message):
        self.log("sending capabilities response")
        self.protocol.send_sccp_message(SCCPCapabilitiesRes())
        self.log("sending button template request message")
        self.protocol.send_sccp_message(SCCPButtonTemplateReq())
        self.log("sending line status request message")
        self.protocol.send_sccp_message(SCCPLineStatReq(1))
        self.log("sending register available lines")
        self.protocol.send_sccp_message(SCCPRegisterAvailableLines())
        self.log("sending time date request message")
        self.protocol.send_sccp_message(SCCPTimeDateReq())

    def on_define_timedate(self, message):
        self.log('define time and date')
        self.datetime_picker.set_datetime(message.day, message.month, message.year, message.hour, message.minute, message.seconds)

    def on_set_speaker_mode(self, message):
        self.log('set speaker mode ' + str(message.mode))

    def on_call_state(self, message):
        self.log('call state line : ' + str(message.line) + ' for callId '+ str(message.callId) + ' is ' + str(SCCPCallState.sccp_channelstates[message.callState]))
        self.current_line = message.line
        self.current_call_id = message.callId
        self.callState = message.callState
        self.call_in_progress = message.callState == SCCPCallState.SCCP_CHANNELSTATE_CONNECTED
        self.ringing = message.callState == SCCPCallState.SCCP_CHANNELSTATE_RINGING
        self.call_waiting = message.callState == SCCPCallState.SCCP_CHANNELSTATE_CALLWAITING
        self.messages_received.append(message.to_str())
        self.states_history.append(SCCPCallState.sccp_channelstates[message.callState])

        for callHandler in self.call_handler:
            callHandler.handle_call(message.line, message.callId, message.callState)

    def on_line_stat(self, message):
        self.log('line stat ' + str(message.line) + ' : ' + message.dirNumber.decode('utf-8'))
        self.displayHandler.display_line_info(message.line,message.dirNumber)

    def on_start_tone(self, message):
        self.log('start tone : ' + str(message.tone) + ' timeout ' + str(message.toneTimeout) + ' line ' + str(message.line) + ' for callId ' + str(message.callId))

    def on_activate_call_plane(self, message):
        self.log('Activate call plane on line ' + str(message.line))

    def on_dialpad_button_pushed(self, car):
        self.log("dialed : " + car)
        if (car == '#'):
            event = 15
        elif (car == '*'):
            event = 14
        else:
            event = int(car)
        message = SCCPKeyPadButton(event)
        self.protocol.send_sccp_message(message)

    def dial(self, number_to_dial):
        self.log('dialing : ' + str(number_to_dial))
        self.protocol.send_sccp_message(SCCPSoftKeyEvent(SKINNY_LBL_NEWCALL))
        for digit in number_to_dial:
            self.on_dialpad_button_pushed(digit)

    def on_soft_key(self, event):
        self.log('on soft key ' + str(event))
        if (event != "SKINNY_LBL_NEWCALL"):
            message = SCCPSoftKeyEvent(event, self.current_line, self.current_call_id)
        else:
            message = SCCPSoftKeyEvent(event)
        self.protocol.send_sccp_message(message)

    async def answer_call(self):
        self.on_soft_key(SKINNY_LBL_ANSWER)

    def end_call(self):
        message = SCCPSoftKeyEvent(SKINNY_LBL_ENDCALL, self.current_line, self.current_call_id)
        self.protocol.send_sccp_message(message)
