from device import *

class ReadableDevice(Device):

    def get_label(self):
        return 'Dummy value'

    def read(self):
        return self.value

