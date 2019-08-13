'''
Created on Aug 13, 2019

@author: nballas
'''
from sccp.sccpmessage import SCCPMessage
from sccp.sccpmessagetype import SCCPMessageType
from struct import unpack

class SCCPCloseReceiveChannel(SCCPMessage):

    def __init__(self):
        SCCPMessage.__init__(self, SCCPMessageType.CloseReceiveChannel)

    def unpack(self, buffer):
        self.conference_id = unpack("I",buffer[:4])[0]
        self.party_id = unpack("I",buffer[4:8])[0]
        self.conference_id_1 = unpack("I",buffer[8:12])[0]