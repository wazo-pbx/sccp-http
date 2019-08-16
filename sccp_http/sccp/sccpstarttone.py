'''
Created on Jun 17, 2011

@author: lebleu1
'''
from sccp_http.sccp.sccpmessage import SCCPMessage
from sccp_http.sccp.sccpmessagetype import SCCPMessageType
from struct import unpack

class SCCPStartTone(SCCPMessage):

    def __init__(self):
        SCCPMessage.__init__(self, SCCPMessageType.StartToneMessage)


    def unpack(self, buffer):
        datas = unpack('IIII',buffer[0:16])
        self.tone = datas[0]
        self.toneTimeout=datas[1]
        self.line=datas[2]
        self.callId=datas[3]
