'''
Created on Jun 14, 2011

@author: lebleu1
'''
from sccp.sccpmessage import SCCPMessage
from sccp.sccpmessagetype import SCCPMessageType
from struct import unpack


class SCCPRegisterAck(SCCPMessage):


    def __init__(self):
        SCCPMessage.__init__(self, SCCPMessageType.RegisterAckMessage)
        self.keep_alive_interval = 50
        self.date_template = ""
        self.secondarykeep_alive_interval = 32


    def unpack(self, buffer):
        self.keep_alive_interval = unpack("I",buffer[:4])[0]
        self.date_template = buffer[4:].split(b"\x00")[0]
        enddate_template =  buffer[4:].find(b"\x00")

        bufferLeft = buffer[4+enddate_template+3:]
        self.secondarykeep_alive_interval = unpack("I",bufferLeft[:4])[0]
