# Copyright 2011-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import struct

class SCCPMessage:
    '''
    Sccp message
    '''

    def __init__(self, sccp_message_type):
        self.sccp_message_type = sccp_message_type
        self.reserved = 0x00

    def __eq__(self, other):
        if (self.__class__.__name__ != other.__class__.__name__):
            return False
        return self.sccp_message_type == other.sccp_message_type

    def pack(self):
        return struct.pack("II",self.reserved,self.sccp_message_type)

    def unpack(self, buffer):
        self.buffer = buffer

    def to_str(self):
        return "SCCPMessage : " + hex(self.sccp_message_type)
