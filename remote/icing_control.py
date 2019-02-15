#!/usr/bin/env python3

from rpyc_classic import *
from switch_device import *

class IcingControl(SwitchDevice):
    def get_name(self):
        return 'Icing control'

    def get_label(self):
        return 'Flavour'

    def get_on_label(self):
        return 'Stawberry'

    def get_off_label(self):
        return 'Chocolate'

my_device = IcingControl()
my_device.value = False

ClassicServer.host = '127.0.0.4'
ClassicServer.run()

