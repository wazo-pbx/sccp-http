'''
Created on Jun 14, 2011

@author: lebleu1
'''

from struct import unpack
from sccp.sccpmessagetype import SCCPMessageType
from sccp.sccpregisterack import SCCPRegisterAck
from sccp.sccpmessage import SCCPMessage
from sccp.sccpcapabilitiesreq import SCCPCapabilitiesReq
from sccp.sccpkeepaliveack import SCCPKeepAliveAck
from sccp.sccpdefinetimedate import SCCPDefineTimeDate
from sccp.sccpsetspeakermode import SCCPSetSpeakerMode
from sccp.sccpcallstate import SCCPCallState
from sccp.sccpactivatecallplane import SCCPActivateCallPlane
from sccp.sccpstarttone import SCCPStartTone
from sccp.sccplinestat import SCCPLineStat
from sccp.sccpopenreceivechannel import SCCPOpenReceiveChannel

class MessageFactory():
    '''
    sccp message factory create message from received buffer
    '''

    messages = {
                SCCPMessageType.RegisterAckMessage: SCCPRegisterAck,
                SCCPMessageType.CapabilitiesReqMessage: SCCPCapabilitiesReq,
                SCCPMessageType.KeepAliveAckMessage: SCCPKeepAliveAck,
                SCCPMessageType.DefineTimeDate: SCCPDefineTimeDate,
                SCCPMessageType.SetSpeakerModeMessage: SCCPSetSpeakerMode,
                SCCPMessageType.CallStateMessage: SCCPCallState,
                SCCPMessageType.ActivateCallPlaneMessage: SCCPActivateCallPlane,
                SCCPMessageType.StartToneMessage: SCCPStartTone,
                SCCPMessageType.LineStatMessage:SCCPLineStat,
                SCCPMessageType.OpenReceiveChannel:SCCPOpenReceiveChannel}

    def __init__(self):
        '''
        '''
    def create(self, buffer):
        message_type = unpack("I", buffer[4:8])[0]
        msg = SCCPMessage(message_type)

        if message_type in self.messages:
            msg = self.messages[message_type]()

        return msg
