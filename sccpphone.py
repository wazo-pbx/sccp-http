'''
Created on Jun 20, 2011

@author: lebleu1
'''
from network.sccpclient import SCCPClient
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

def make_sccp_packet(msg):
    return struct.pack("<L", len(msg.pack())) + msg.pack() + b"\x00\x00\x00\x00"

class SCCPPhone():
    '''
    Main sccp phone class
    '''


    def __init__(self,host,deviceName):
        self.host = host
        self.deviceName = deviceName
        self.callHandlers = set()

    def setLogger(self,logger):
        self.log = logger

    async def run(self, protocol):
        self.complete_construction(protocol)
        protocol.client_ready(self)

    def setTimerProvider(self,timerProvider):
        self.timerProvider = timerProvider

    def setRegisteredHandler(self,registeredHandler):
        self.registeredHandler = registeredHandler

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
        self.protocol.handleUnknownMessage(self.onUnknownMessage)
        self.protocol.addHandler(SCCPMessageType.RegisterAckMessage,self.onRegisteredAck)
        self.protocol.addHandler(SCCPMessageType.CapabilitiesReqMessage,self.onCapabilitiesReq)
        self.protocol.addHandler(SCCPMessageType.KeepAliveAckMessage,self.onKeepAliveAck)
        self.protocol.addHandler(SCCPMessageType.DefineTimeDate,self.onDefineTimeDate)
        self.protocol.addHandler(SCCPMessageType.SetSpeakerModeMessage,self.onSetSpeakerMode)
        self.protocol.addHandler(SCCPMessageType.CallStateMessage,self.onCallState)
        self.protocol.addHandler(SCCPMessageType.ActivateCallPlaneMessage,self.onActivateCallPlane)
        self.protocol.addHandler(SCCPMessageType.StartToneMessage,self.onStartTone)
        self.protocol.addHandler(SCCPMessageType.LineStatMessage,self.onLineStat)
        self.protocol.addHandler(SCCPMessageType.RegisterRejectMessage,self.onRegisterRejectMessage)
        self.protocol.addHandler(SCCPMessageType.SetRingerMessage,self.onSetRingerMessage)

    def register(self):
        print('registering...')
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
        self.client.sendSccpMessage(message)

    def onUnknownMessage(self,message):
        self.log('receive unkown message ' + message.toStr())

    def onRegisteredAck(self,registerAck):
        self.log("sccp phone registered")
        self.log("--          keepAliveInterval : " + registerAck.keepAliveInterval)
        self.log("--               dateTemplate : " + registerAck.dateTemplate)
        self.log("-- secondaryKeepAliveInterval : " + registerAck.secondaryKeepAliveInterval)
        self.timerProvider.createTimer(registerAck.keepAliveInterval,self.onKeepAliveTimer)
        self.registeredHandler.onRegistered()


    def onKeepAliveAck(self,message):
        self.log("Keepalive ack")

    def onCapabilitiesReq(self,message):
        self.log("sending capabilities response")
        self.client.sendSccpMessage(SCCPCapabilitiesRes())
        self.log("sending button template request message")
        self.client.sendSccpMessage(SCCPButtonTemplateReq())
        self.log("sending line status request message")
        self.client.sendSccpMessage(SCCPLineStatReq(1))
        self.log("sending register available lines")
        self.client.sendSccpMessage(SCCPRegisterAvailableLines())
        self.log("sending time date request message")
        self.client.sendSccpMessage(SCCPTimeDateReq())


    def onDefineTimeDate(self,message):
        self.log('define time and date')
        self.dateTimePicker.setDateTime(message.day,message.month,message.year,message.hour,message.minute,message.seconds)

    def onSetSpeakerMode(self,message):
        self.log('set speaker mode ' + message.mode)

    def onCallState(self,message):
        self.log('call state line : ' + message.line + ' for callId '+ message.callId + ' is ' + SCCPCallState.sccp_channelstates[message.callState])
        self.currentLine = message.line
        self.currentCallId=message.callId
        self.callState=message.callState

        for callHandler in self.callHandlers:
            callHandler.handleCall(message.line,message.callId,message.callState)

    def onLineStat(self,message):
        self.log('line stat ' + message.line + ' : ' + message.dirNumber)
        self.displayHandler.displayLineInfo(message.line,message.dirNumber)

    def onStartTone(self,message):
        self.log('start tone : '+message.tone + ' timeout ' + message.toneTimeout + ' line ' + message.line + ' for callId '+ message.callId)

    def onActivateCallPlane(self,message):
        self.log('Activate call plane on line '+message.line)

    def onDialPadButtonPushed(self,car):
        self.log("dialed : " + car)
        if (car == '#'):
            event = 15
        elif (car == '*'):
            event = 14
        else:
            event = int(car)
        message = SCCPKeyPadButton(event)
        self.client.sendSccpMessage(message)

    def dial(self,numberToDial):
        self.log('dialing : ' + numberToDial)
        self.client.sendSccpMessage(SCCPSoftKeyEvent(SKINNY_LBL_NEWCALL))
        for digit in numberToDial:
            self.onDialPadButtonPushed(digit)

    def onSoftKey(self,event):
        self.log('on soft key ' + event)
        if (event != "SKINNY_LBL_NEWCALL"):
            message = SCCPSoftKeyEvent(event,self.currentLine,self.currentCallId)
        else:
            message = SCCPSoftKeyEvent(event)
        self.client.sendSccpMessage(message)

    def answerCall(self):
        self.onSoftKey(SKINNY_LBL_ANSWER)

    def endCall(self,line,callId):
        message = SCCPSoftKeyEvent(SKINNY_LBL_ENDCALL,line,callId)
        self.client.sendSccpMessage(message)
