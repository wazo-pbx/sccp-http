'''
Created on Jun 14, 2011

@author: lebleu1
'''
from struct import pack
class IpAddress:

    def __init__(self, address):
        self.address = address

    def __eq__(self,obj):
        return self.address == obj.address

    def __ne__(self,obj):
        return self.address != obj.address

    def pack(self):
        elements = self.address.split('.')
        packed = b''
        for byte in elements:
            packed += pack("B", int(byte))
        return packed
