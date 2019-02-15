#!/usr/bin/env python3

from rpyc_classic import *
from writeable_device import *

class Sweentess(WriteableDevice):
    def get_name(self):
        return 'Sweetness control'

    def get_label(self):
        return '% of donut that is sugar'

my_device = Sweentess()
my_device.write('50')

ClassicServer.host = '127.0.0.3'
ClassicServer.run()

