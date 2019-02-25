#!/usr/bin/env python3 # script to interpret python language

from rpyc_classic import * # from the rpyc_classic method import all lib?
from writeable_device import *

class FreezeTime(WriteableDevice): # defining a class called sweentess with argument WriteableDevice passed in for use later
    def get_name(self):
        return 'Freeze control'

    def get_label(self):
        return '% of food that is frozen'

my_device = FreezeTime()
my_device.write('0:20:00') # freeze time is 0 hours and 20 minutes to freeze a product

ClassicServer.host = '127.0.0.3'
ClassicServer.run()

