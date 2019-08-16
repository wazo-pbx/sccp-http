# Copyright 2011-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from sccp_http.sccp.sccpmessage import SCCPMessage
from sccp_http.sccp.sccpmessagetype import SCCPMessageType
from struct import pack


class SCCPLineStatReq(SCCPMessage):


    def __init__(self,line):
        SCCPMessage.__init__(self, SCCPMessageType.LineStatReqMessage)
        self.line = line



    def pack(self):
        strPack = SCCPMessage.pack(self)
        strPack = strPack + pack("L",self.line)
        return strPack
