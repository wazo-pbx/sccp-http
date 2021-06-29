# Copyright 2011-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from struct import unpack
from sccp_http.sccp.sccpmessagetype import SCCPMessageType
from sccp_http.sccp.sccpregisterack import SCCPRegisterAck
from sccp_http.sccp.sccpmessage import SCCPMessage
from sccp_http.sccp.sccpcapabilitiesreq import SCCPCapabilitiesReq
from sccp_http.sccp.sccpkeepaliveack import SCCPKeepAliveAck
from sccp_http.sccp.sccpdefinetimedate import SCCPDefineTimeDate
from sccp_http.sccp.sccpsetspeakermode import SCCPSetSpeakerMode
from sccp_http.sccp.sccpcallstate import SCCPCallState
from sccp_http.sccp.sccpactivatecallplane import SCCPActivateCallPlane
from sccp_http.sccp.sccpstarttone import SCCPStartTone
from sccp_http.sccp.sccplinestat import SCCPLineStat
from sccp_http.sccp.sccpopenreceivechannel import SCCPOpenReceiveChannel
from sccp_http.sccp.sccpclosereceivechannel import SCCPCloseReceiveChannel

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
                SCCPMessageType.OpenReceiveChannel:SCCPOpenReceiveChannel,
                SCCPMessageType.CloseReceiveChannel:SCCPCloseReceiveChannel}

    def __init__(self):
        '''
        '''
    def create(self, buffer):
        message_type = unpack("I", buffer[4:8])[0]
        msg = SCCPMessage(message_type)

        if message_type in self.messages:
            msg = self.messages[message_type]()

        return msg
