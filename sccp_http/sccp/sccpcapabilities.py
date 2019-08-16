'''
Created on Jun 14, 2011

@author: lebleu1
'''
from sccp_http.sccp.sccpmessage import SCCPMessage
from sccp_http.sccp.sccpmessagetype import SCCPMessageType
from struct import pack
from sccp_http.network.ip_address import IpAddress

class SCCPCapabilitiesRes(SCCPMessage):
    '''
    sccp register message
    '''
    def __init__(self):
        '''
        Constructor
        '''
        SCCPMessage.__init__(self, SCCPMessageType.CapabilitiesResMessage)
        self.capCount = 3
        self.payLoads = b"\x19\x00\x00\x00\x78\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        self.payLoads += b"\x04\x00\x00\x00\x28\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        self.payLoads += b"\x02\x00\x00\x00\x28\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"

    def pack(self):
        strPack = SCCPMessage.pack(self)
        strPack = strPack + pack("H",self.capCount) + pack("H",0)
        strPack = strPack + self.payLoads
        return strPack
