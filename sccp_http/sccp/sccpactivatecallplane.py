'''
Created on Jun 14, 2011

@author: lebleu1
'''
from sccp_http.sccp.sccpmessage import SCCPMessage
from sccp_http.sccp.sccpmessagetype import SCCPMessageType
from struct import unpack


class SCCPActivateCallPlane(SCCPMessage):


    def __init__(self):
        SCCPMessage.__init__(self, SCCPMessageType.ActivateCallPlaneMessage)

    def unpack(self, buffer):
        self.line = unpack("L", buffer[:4])[0]
