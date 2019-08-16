# Copyright 2011-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from sccp_http.sccp.sccpmessage import SCCPMessage
from sccp_http.sccp.sccpmessagetype import SCCPMessageType
from struct import pack


class SCCPKeyPadButton(SCCPMessage):


    def __init__(self,button):
        SCCPMessage.__init__(self, SCCPMessageType.KeypadButtonMessage)
        self.button = button


    def __eq__(self,other):
        return SCCPMessage.__eq__(self, other) and self.button == other.button

    def pack(self):
        strPack = SCCPMessage.pack(self)
        strPack = strPack + pack("L",self.button)
        return strPack
