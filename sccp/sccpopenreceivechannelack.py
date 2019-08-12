'''
Created on Aug 12, 2019

@author: nballas
'''
from sccp.sccpmessage import SCCPMessage
from sccp.sccpmessagetype import SCCPMessageType
from struct import pack, unpack

class SCCPOpenReceiveChannelAck(SCCPMessage):

    def __init__(self):
        SCCPMessage.__init__(self, SCCPMessageType.OpenReceiveChannelAck)
        self.port_number = 26446

    def pack(self):
        packed = SCCPMessage.pack(self)
        packed += pack("I", 0)  # media reception status OK
        packed += self.ip_addr.pack()  # where from?
        packed += pack("I", self.port_number)  # where from?

        return packed
