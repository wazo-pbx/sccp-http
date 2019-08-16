# Copyright 2011-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from sccp_http.sccp.sccpmessage import SCCPMessage
from sccp_http.sccp.sccpmessagetype import SCCPMessageType


class SCCPCapabilitiesReq(SCCPMessage):


    def __init__(self):
        SCCPMessage.__init__(self, SCCPMessageType.CapabilitiesReqMessage)
