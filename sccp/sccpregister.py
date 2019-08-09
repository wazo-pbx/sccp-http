'''
Created on Jun 14, 2011

@author: lebleu1
'''
from sccp.sccpmessage import SCCPMessage
from sccp.sccpmessagetype import SCCPMessageType
from struct import pack
from network.ip_address import IpAddress

class SCCPRegister(SCCPMessage):
    '''
    sccp register message
    '''
    TelecasterBus = 0x08
    MAXSTREAMS = 0
    STATION_INSTANCE = 1
    STATION_USERID = 0


    def __init__(self, device_name, ip_address):
        '''
        Constructor
        '''
        SCCPMessage.__init__(self, SCCPMessageType.RegisterMessage)
        self.device_name = device_name
        self.ip_address = IpAddress(ip_address)
        self.stationUserId = self.STATION_USERID
        self.station_instance = self.STATION_INSTANCE
        self.device_type = self.TelecasterBus
        self.max_streams = self.MAXSTREAMS

    def __eq__(self,obj):
        if (self.device_name != obj.device_name):
            return False
        if (self.ip_address != obj.ip_address):
            return False
        return True


    def pack(self):
        packed = SCCPMessage.pack(self)
        packed += self.device_name.encode('utf-8') + b'\x00'
        packed += pack("II",self.stationUserId,self.station_instance)
        packed += self.ip_address.pack()
        packed += pack("III",self.device_type,self.max_streams,0)
        packed += b'\x0B'+ b'\x00'+ b'\x60'+ b'\x85'
        packed += pack('IIII',0,0,0,0)
        return packed
