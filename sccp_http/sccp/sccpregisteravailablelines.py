# Copyright 2011-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from sccp_http.sccp.sccpmessage import SCCPMessage
from sccp_http.sccp.sccpmessagetype import SCCPMessageType
from struct import pack

class SCCPRegisterAvailableLines(SCCPMessage):
    '''
    sccp register message
    '''
    def __init__(self):
        '''
        Constructor
        '''
        SCCPMessage.__init__(self, SCCPMessageType.RegisterAvailableLinesMessage)
        self.nboflines = 1

    def pack(self):
        strPack = SCCPMessage.pack(self)
        strPack = strPack + pack("L",self.nboflines)
        return strPack
