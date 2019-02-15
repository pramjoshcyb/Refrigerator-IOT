#!/usr/bin/env python3

from readable_device import *

class SwitchDevice(ReadableDevice):

    def get_on_label(self):
        return 'On'

    def get_off_label(self):
        return 'Off'

    def turn_on(self):
        print('turning on')
        self.value = True

    def turn_off(self):
        print('turning off')
        self.value = False
