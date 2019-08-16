# Copyright 2011-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from sccp_http.sccp.sccpmessage import SCCPMessage
from sccp_http.sccp.sccpmessagetype import SCCPMessageType
from struct import unpack

class SCCPOpenReceiveChannel(SCCPMessage):

    def __init__(self):
        SCCPMessage.__init__(self, SCCPMessageType.OpenReceiveChannel)

    def unpack(self, buffer):
        self.conference_id = unpack("I",buffer[:4])[0]
        self.pass_through_party_id = unpack("I",buffer[4:8])[0]
        self.millisecond_packed_size = unpack("I",buffer[8:12])[0]
        self.compression_type = unpack("I",buffer[12:16])[0]
