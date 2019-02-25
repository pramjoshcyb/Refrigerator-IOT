#!/usr/bin/env python3 # interprets the python3 language to execute the script

from rpyc_classic import * # from the remote proc call import all libraries?
from switch_device import *# from the switch_device argument import all libraries?

# presuming that SwitchDevice is a method to switch the GUI to another IOT
class TemperatureControl(SwitchDevice): # defined a class called IcingControl which passes in the argument SwitchDevice
    def get_name(self): # method get_name, instance of class, where self argument is passed in to access attributes of the class
        return 'Low -5'

    def get_label(self): # defined another method get_label which also gets the self argument to grab the attributes of the class
        return 'Medium -10'

    def get_on_label(self): # defined a third method called get_on_label which also gets passed self and returns string strawberry
        return 'Extreme -30'

    def get_off_label(self): # get_off_label which returns the string Chocolate 
        return 'Severe -40'

my_device = TemperatureControl() # defined variable called my_device and assigned IceControl() method from another page
my_device.value = False # my_device method accesses value which is returned as false

ClassicServer.host = '127.0.0.4' # method to get the client to connect to this IP Address
ClassicServer.run() # Runs the server 

