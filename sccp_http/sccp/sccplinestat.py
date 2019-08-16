# Copyright 2011-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from sccp_http.sccp.sccpmessage import SCCPMessage
from sccp_http.sccp.sccpmessagetype import SCCPMessageType
from struct import unpack


class SCCPLineStat(SCCPMessage):


    def __init__(self):
        SCCPMessage.__init__(self, SCCPMessageType.LineStatMessage)
        self.line = 0
        self.dirNumber = ""


    def unpack(self,buffer):
        self.line = unpack("I",buffer[:4])[0]
        self.dirNumber = buffer[4:].split(b"\x00")[0]
