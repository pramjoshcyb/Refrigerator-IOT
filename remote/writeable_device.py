from readable_device import *

class WriteableDevice(ReadableDevice):

    def write(self, value):
        self.value = value
