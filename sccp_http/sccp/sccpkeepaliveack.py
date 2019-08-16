'''
Created on Jun 14, 2011

@author: lebleu1
'''
from sccp_http.sccp.sccpmessage import SCCPMessage
from sccp_http.sccp.sccpmessagetype import SCCPMessageType


class SCCPKeepAliveAck(SCCPMessage):


    def __init__(self):
        SCCPMessage.__init__(self, SCCPMessageType.KeepAliveAckMessage)
