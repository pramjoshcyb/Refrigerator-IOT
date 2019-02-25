from device import * # from device import all libraries

class ReadableDevice(Device): # class is defined which reads the device

    def get_label(self): # method to get label which returns the string Dummy value 
        return 'refrigerator value'

    def read(self): # read method defined which returns the self.value to access the value of the self attribute?
        return self.value

