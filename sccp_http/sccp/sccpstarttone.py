# Copyright 2011-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from sccp_http.sccp.sccpmessage import SCCPMessage
from sccp_http.sccp.sccpmessagetype import SCCPMessageType
from struct import unpack

class SCCPStartTone(SCCPMessage):

    def __init__(self):
        SCCPMessage.__init__(self, SCCPMessageType.StartToneMessage)


    def unpack(self, buffer):
        datas = unpack('IIII',buffer[0:16])
        self.tone = datas[0]
        self.toneTimeout=datas[1]
        self.line=datas[2]
        self.callId=datas[3]
