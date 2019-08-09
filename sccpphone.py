'''
Created on Jun 20, 2011

@author: lebleu1
'''
from sccp.sccpmessagetype import SCCPMessageType
from sccp.sccpregister import SCCPRegister
from sccp.sccpcapabilities import SCCPCapabilitiesRes
from sccp.sccpbuttontemplatereq import SCCPButtonTemplateReq
from sccp.sccpregisteravailablelines import SCCPRegisterAvailableLines
from sccp.sccptimedatereq import SCCPTimeDateReq
from sccp.sccpcallstate import SCCPCallState
from sccp.sccpkeypadbutton import SCCPKeyPadButton
from sccp.sccpsoftkeyevent import SCCPSoftKeyEvent
from sccp.sccpmessage import SCCPMessage
from sccp.sccplinestatreq import SCCPLineStatReq
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


    def __init__(self,host,deviceName):
        self.host = host
        self.deviceName = deviceName
        self.callHandlers = set()
        self.registered = False
        self.call_in_progress = False

    def setLogger(self,logger):
        self.log = logger

    async def run(self, protocol):
        self.complete_construction(protocol)
        protocol.client_ready(self)

    def setTimerProvider(self,timerProvider):
        self.timerProvider = timerProvider

    def setRegisteredHandler(self,registered_handler):
        self.registeredHandler = registered_handler
        self.registeredHandler.registree = self

    def setDateTimePicker(self,dateTimePicker):
        self.dateTimePicker = dateTimePicker

    def setDisplayHandler(self,displayHandler):
        self.displayHandler = displayHandler

    def addCallHandler(self,callHandler):
        self.log(self.deviceName + ' adding call handler')
        self.callHandlers.add(callHandler)

    def complete_construction(self, protocol):
        self.log('completing construction')
        self.protocol = protocol
        self.protocol.handle_unknown_message(self.onUnknownMessage)
        self.protocol.add_handler(SCCPMessageType.RegisterAckMessage,self.onRegisteredAck)
        self.protocol.add_handler(SCCPMessageType.CapabilitiesReqMessage,self.onCapabilitiesReq)
        self.protocol.add_handler(SCCPMessageType.KeepAliveAckMessage,self.onKeepAliveAck)
        self.protocol.add_handler(SCCPMessageType.DefineTimeDate,self.onDefineTimeDate)
        self.protocol.add_handler(SCCPMessageType.SetSpeakerModeMessage,self.onSetSpeakerMode)
        self.protocol.add_handler(SCCPMessageType.CallStateMessage,self.onCallState)
        self.protocol.add_handler(SCCPMessageType.ActivateCallPlaneMessage,self.onActivateCallPlane)
        self.protocol.add_handler(SCCPMessageType.StartToneMessage,self.onStartTone)
        self.protocol.add_handler(SCCPMessageType.LineStatMessage,self.onLineStat)
        self.protocol.add_handler(SCCPMessageType.RegisterRejectMessage,self.onRegisterRejectMessage)
        self.protocol.add_handler(SCCPMessageType.SetRingerMessage,self.onSetRingerMessage)

    def register(self):
        self.log('registering device: ' + self.deviceName)
        register_message = SCCPRegister(self.deviceName, self.host)
        self.protocol.send_sccp_message(register_message)

    def on_sccp_connect_success(self):
        # reason is a twisted.python.failure.Failure  object
        self.register()

    def on_sccp_connect_fail(self, reason):
        # reason is a twisted.python.failure.Failure  object
        self.log('Connection failed: %s' % reason.getErrorMessage())

    def onRegisterRejectMessage(self, message):
        self.log('register failed ' + message.toStr())

    def onSetRingerMessage(self, message):
        self.log('ringer mode: ' + message.toStr())

    def onKeepAliveTimer(self):
        self.log('on keep alive')
        message = SCCPMessage(SCCPMessageType.KeepAliveMessage)
        self.protocol.send_sccp_message(message)

    def onUnknownMessage(self,message):
        self.log('receive unkown message ' + message.toStr())

    def onRegisteredAck(self,registerAck):
        self.log("sccp phone registered")
        self.log("--          keepAliveInterval : " + str(registerAck.keepAliveInterval))
        self.log("--               dateTemplate : " + str(registerAck.dateTemplate))
        self.log("-- secondaryKeepAliveInterval : " + str(registerAck.secondaryKeepAliveInterval))
        self.timerProvider.createTimer(registerAck.keepAliveInterval,self.onKeepAliveTimer)
        self.registeredHandler.onRegistered()


    def onKeepAliveAck(self,message):
        self.log("Keepalive ack")

    def onCapabilitiesReq(self,message):
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



    def onDefineTimeDate(self,message):
        self.log('define time and date')
        self.dateTimePicker.setDateTime(message.day, message.month, message.year, message.hour, message.minute, message.seconds)

    def onSetSpeakerMode(self,message):
        self.log('set speaker mode ' + str(message.mode))

    def onCallState(self,message):
        self.log('call state line : ' + str(message.line) + ' for callId '+ str(message.callId) + ' is ' + str(SCCPCallState.sccp_channelstates[message.callState]))
        self.currentLine = message.line
        self.currentCallId = message.callId
        self.callState = message.callState
        self.call_in_progress = message.callState == SCCPCallState.SCCP_CHANNELSTATE_ONHOOK

        for callHandler in self.callHandlers:
            callHandler.handleCall(message.line,message.callId,message.callState)

    def onLineStat(self, message):
        self.log('line stat ' + str(message.line) + ' : ' + message.dirNumber.decode('utf-8'))
        self.displayHandler.displayLineInfo(message.line,message.dirNumber)

    def onStartTone(self, message):
        self.log('start tone : ' + str(message.tone) + ' timeout ' + str(message.toneTimeout) + ' line ' + str(message.line) + ' for callId ' + str(message.callId))

    def onActivateCallPlane(self, message):
        self.log('Activate call plane on line ' + str(message.line))

    def onDialPadButtonPushed(self,car):
        self.log("dialed : " + car)
        if (car == '#'):
            event = 15
        elif (car == '*'):
            event = 14
        else:
            event = int(car)
        message = SCCPKeyPadButton(event)
        self.protocol.send_sccp_message(message)

    async def dial(self, number_to_dial):
        self.log('dialing : ' + str(number_to_dial))
        self.protocol.send_sccp_message(SCCPSoftKeyEvent(SKINNY_LBL_NEWCALL))
        for digit in number_to_dial:
            self.onDialPadButtonPushed(digit)

    def onSoftKey(self, event):
        self.log('on soft key ' + str(event))
        if (event != "SKINNY_LBL_NEWCALL"):
            message = SCCPSoftKeyEvent(event,self.currentLine,self.currentCallId)
        else:
            message = SCCPSoftKeyEvent(event)
        self.protocol.send_sccp_message(message)

    def answer_call(self):
        self.call_in_progress = True
        self.onSoftKey(SKINNY_LBL_ANSWER)

    def end_call(self, line, callId):
        message = SCCPSoftKeyEvent(SKINNY_LBL_ENDCALL,line,callId)
        self.protocol.send_sccp_message(message)
        self.call_in_progress = False
