class DeviceAlreadyRegistered(Exception):
    def __init__(self, device=''):
        super().__init__()
        self.message = "already registered device: " + device

class DeviceNotRegistered(Exception):
    def __init__(self):
        super().__init__()
        self.message = "no device registered"

class NoCallInProgress(Exception):
    def __init__(self):
        super().__init__()
        self.message = "no call in progress"
