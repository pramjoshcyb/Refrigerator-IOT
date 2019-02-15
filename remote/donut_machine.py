#!/usr/bin/env python3

from rpyc_classic import *
from switch_device import *

class DonutMachine(SwitchDevice):
    def get_name(self):
        return 'Donut Machine'

    def get_label(self):
        return 'Current state'

my_device = DonutMachine()
my_device.value = False

ClassicServer.host = '127.0.0.2'
ClassicServer.run()

