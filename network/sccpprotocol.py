import asyncio
import struct
from sccp.messagefactory import MessageFactory

def make_sccp_packet(msg):
    return struct.pack("<L", len(msg.pack())) + msg.pack() + b"\x00\x00\x00\x00"

class SCCPProtocol(asyncio.Protocol):

    def __init__(self):
        super().__init__()
        self.structFormat = "<L"
        self.prefixLength = struct.calcsize(self.structFormat)
        self.trailingNbOfBytes = 4
        self.messageFactory = MessageFactory()
        self.messageHandlers={}
        self.UNKNOWN_KEY = 'UNKNOWN'
        self.message_factory = MessageFactory()
        self.stop_flag = False
        self.recvd = b''

    def connection_made(self, transport):
        self.transport = transport

    def addHandler(self, messageType, callback):
        self.messageHandlers[messageType] = callback

    def handleUnknownMessage(self, unknownHandler):
        self.messageHandlers[self.UNKNOWN_KEY] = unknownHandler

    def data_received(self, data):
        msg = self.message_factory.create(data)
        self.handleMessage(msg)

    def client_ready(self, client):
        self.client = client
        self.client.on_sccp_connect_success()

    def make_sccp_packet(self, msg):
        return struct.pack(self.structFormat, len(msg.pack())) + msg.pack() + b"\x00\x00\x00\x00"

    def send_sccp_message(self, msg):
            self.send_data(self.make_sccp_packet(msg))

    def connection_lost(self, exc):
        print('The server closed the connection')
        self.transport.close()

    def stringReceived(self, s):
        message = self.messageFactory.create(s)
        message.unPack(s[8:])
        self.handleMessage(message)

    def clientConnectionLost(self, connector, reason):
        print('Lost connection.  Reason:', reason)

    def addHandler(self, messageType, callback):
        self.messageHandlers[messageType] = callback

    def handleUnknownMessage(self, unknownHandler):
        self.messageHandlers[self.UNKNOWN_KEY] = unknownHandler

    def handleMessage(self,message):
        if message.sccpmessageType in self.messageHandlers:
            self.messageHandlers[message.sccpmessageType](message)
        else:
            if self.UNKNOWN_KEY in self.messageHandlers:
                self.messageHandlers[self.UNKNOWN_KEY](message)
            else:
                print("ERROR unknown message " + str(message.sccpmessageType) + " no handler")

    def send_data(self, data):
        self.transport.write(data)
