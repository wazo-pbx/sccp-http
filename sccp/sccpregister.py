'''
Created on Jun 14, 2011

@author: lebleu1
'''
from sccp.sccpmessage import SCCPMessage
from sccp.sccpmessagetype import SCCPMessageType
from struct import pack
from network.ipAddress import IpAddress

class SCCPRegister(SCCPMessage):
    '''
    sccp register message
    '''
    TelecasterBus=0x08
    MAXSTREAMS=0
    STATION_INSTANCE=1
    STATION_USERID=0


    def __init__(self,deviceName,ipAddress):
        '''
        Constructor
        '''
        SCCPMessage.__init__(self, SCCPMessageType.RegisterMessage)
        self.deviceName=deviceName
        self.ipAddress = IpAddress(ipAddress)
        self.stationUserId=self.STATION_USERID
        self.stationInstance=self.STATION_INSTANCE
        self.deviceType=self.TelecasterBus
        self.maxStreams=self.MAXSTREAMS

    def __eq__(self,obj):
        if (self.deviceName != obj.deviceName):
            return False
        if (self.ipAddress != obj.ipAddress):
            return False
        return True


    def pack(self):
        packed = SCCPMessage.pack(self)
        packed += self.deviceName.encode('utf-8') + b'\x00'
        packed += pack("II",self.stationUserId,self.stationInstance)
        packed += self.ipAddress.pack()
        packed += pack("III",self.deviceType,self.maxStreams,0)
        packed += b'\x0B'+ b'\x00'+ b'\x60'+ b'\x85'
        packed += pack('IIII',0,0,0,0)
        print(packed)
        return packed
