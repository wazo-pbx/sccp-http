'''
Created on Jun 14, 2011

@author: lebleu1
'''
from sccp_http.sccp.sccpmessage import SCCPMessage
from sccp_http.sccp.sccpmessagetype import SCCPMessageType
from struct import unpack


class SCCPSetSpeakerMode(SCCPMessage):


    def __init__(self):
        SCCPMessage.__init__(self, SCCPMessageType.SetSpeakerModeMessage)
        self.mode = 0


    def unpack(self,buffer):
        self.mode = unpack("I",buffer[:4])[0]
