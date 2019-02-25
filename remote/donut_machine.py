#!/usr/bin/env python3 
# the above means that the script is executable which the script then calls the language's interpreter to run the code inside the script
# absolute path to find python3 language interpreter 

from rpyc_classic import * # importing rpc
from switch_device import *# inheritance import

class RefrigeratorMachine(SwitchDevice): # declared a class called DonutMachine with an argument called SwitchDevice
    def get_name(self): # method called get_name which uses the self attribute which refers to instance attributes, to return a Donut Machine
        return 'Refrigerator Machine' # self points the instance which it was called

    def get_label(self): # method called get_label which uses the self attribute and returns the current condition of the GUI
        return 'Current state'

my_device = RefrigeratorMachine() # declared a variable called my-device and assigned the DOnutMachine() method (link to other file)
my_device.value = False # sets the value of the DonutMachine() method to false value

ClassicServer.host = '127.0.0.2' # client runs on the local address 
ClassicServer.run() # method to call the server and run it 

