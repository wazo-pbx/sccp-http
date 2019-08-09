import asyncio
import struct
from sccp.messagefactory import MessageFactory

def make_sccp_packet(msg):
    return struct.pack("<L", len(msg.pack())) + msg.pack() + b"\x00\x00\x00\x00"

class SCCPProtocol(asyncio.Protocol):

    def __init__(self):
        super().__init__()
        self.struct_format = "<L"
        self.prefix_length = struct.calcsize(self.struct_format)
        self.trailing_nb_of_bytes = 4
        self.message_handlers={}
        self.UNKNOWN_KEY = 'UNKNOWN'
        self.message_factory = MessageFactory()
        self.stop_flag = False
        self.received = b''

    def connection_made(self, transport):
        self.transport = transport

    def addHandler(self, message_type, callback):
        self.message_handlers[message_type] = callback

    def handleUnknownMessage(self, unknownHandler):
        self.message_handlers[self.UNKNOWN_KEY] = unknownHandler

    def data_received(self, data):
        self.received += data
        while len(self.received) >= self.prefix_length:
            length, = struct.unpack(self.struct_format, self.received[:self.prefix_length])
            length += self.trailing_nb_of_bytes
            if len(self.received) < length + self.prefix_length:
                break
            packet = self.received[self.prefix_length:length + self.prefix_length]
            self.received = self.received[length + self.prefix_length:]
            msg = self.message_factory.create(packet)
            msg.unPack(packet[8:])
            self.handle_message(msg)

    def client_ready(self, client):
        self.client = client
        self.client.on_sccp_connect_success()

    def make_sccp_packet(self, msg):
        return struct.pack(self.struct_format, len(msg.pack())) + msg.pack() + b"\x00\x00\x00\x00"

    def send_sccp_message(self, msg):
            self.send_data(self.make_sccp_packet(msg))

    def connection_lost(self, exc):
        print('The server closed the connection')
        self.transport.close()

    def add_handler(self, message_type, callback):
        self.message_handlers[message_type] = callback

    def handle_unknown_message(self, unknownHandler):
        self.message_handlers[self.UNKNOWN_KEY] = unknownHandler

    def handle_message(self,message):
        if message.sccpmessageType in self.message_handlers:
            self.message_handlers[message.sccpmessageType](message)
        else:
            if self.UNKNOWN_KEY in self.message_handlers:
                self.message_handlers[self.UNKNOWN_KEY](message)
            else:
                print("ERROR unknown message " + str(message.sccpmessageType) + " no handler")

    def send_data(self, data):
        self.transport.write(data)
