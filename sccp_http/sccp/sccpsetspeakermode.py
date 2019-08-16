# Copyright 2011-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from sccp_http.sccp.sccpmessage import SCCPMessage
from sccp_http.sccp.sccpmessagetype import SCCPMessageType
from struct import unpack


class SCCPSetSpeakerMode(SCCPMessage):


    def __init__(self):
        SCCPMessage.__init__(self, SCCPMessageType.SetSpeakerModeMessage)
        self.mode = 0


    def unpack(self,buffer):
        self.mode = unpack("I",buffer[:4])[0]
