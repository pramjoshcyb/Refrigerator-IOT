from PyQt5.Qt import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import rpyc # importing remote procedure call


class RefrigeratorUI(): # creating a class called RefrigeratorUI 
                # init is a reserved method in python classes, called when an object is created from the class
    def __init__(self): # self represents instance of class DonutUI, which allows to access attributes and methods of class
        self.app = QApplication([]) # initialises the window and constructs an app object
        # instance of the class attribute where app is a local var
        connect_panel = self.create_connect_panel() # declared a var and assigned the self instance for creating panel to it

        window = QWidget() # returns the window for the widget
        layout = QVBoxLayout() # creates a layout for the IOT and qvboxlayout is an object which is added to the widget layout
        layout.addWidget(connect_panel) # layout method is added to the addwidget 
        window.setLayout(layout) #sets the qvboxlayout by calling it from the window method
        window.show() #displays the window


        self.main_layout = layout

        self.window = window

    def create_connect_panel(self): # method for create_connect_panel
        panel = QFrame() # declared panel and assign QFrame widget 
        panel.setFrameShape(QFrame.Panel) # frame for GUI panel
        layout = QVBoxLayout() # layout for the IOT 
        lbl_ip_address = QLabel('Enter IP address or hostname:') # label widget assigned to lbl_ip_address var 
        inp_ip_address = QLineEdit() # QLineEdit() widget assigned to the inp_ip_address variable (input ip)
        inp_ip_address.setText('127.0.0.2') # set the text to connect to host machine, inp_ip_address method is added to set text feature
        btn_connect = QPushButton('Link new device') # declared btn_connect var and assigned QPushButton widget to link the new device
        # qpushbutton gives a command button which commands computer to do some action
        layout.addWidget(lbl_ip_address) # adds the layout to the widget by calling lbl_ip_add that has the label
        layout.addWidget(inp_ip_address)
        layout.addWidget(btn_connect)

        def connect(): # new method connect
            hostname = inp_ip_address.text() # declared hostname var and assigned the input of ip address to it
            connection = rpyc.classic.connect(hostname) # declared connection var and assigned the remote call to connect to the host
            device = connection.modules.__main__.my_device # declared device var and assigned the conn module to it 
            self.add_device_panel(device) # self method to access attribute of the device 

        btn_connect.clicked.connect(connect) # when the link new device btn is clicked it connects to server

        panel.setLayout(layout) # calls layout method to set the panel

        return panel # returns the panel 

    def add_device_panel(self, device): # new method that takes parameters self and device 
        panel = QFrame() # initiates the QFrame widget assigned to the panel of the GUI
        panel.setFrameShape(QFrame.Box) # panel method to set the frame shape in rectangle
        layout = QVBoxLayout()

        lbl_name = QLabel('Device: ' + device.get_name()) # name of device label
        lbl_label = QLabel(device.get_label())

        layout.addWidget(lbl_name)
        layout.addWidget(lbl_label)

        #determine what kind of device
        if hasattr(device, 'turn_on'): #if statement to check attributes if device is a switch
            rad_on = QRadioButton(device.get_on_label()) # rad_on is declared and radio button on is assigned
            rad_off = QRadioButton(device.get_off_label()) # rad_off is declared and radio button off is assigned
            layout.addWidget(rad_on) # attribute layout.addwidget is called to input the radio button ON
            layout.addWidget(rad_off) # attribute layout.addwidget is called to input the radio button OFF

            if device.read() == True: # if statement to determine if the device is connected 
                rad_on.setChecked(True) # if rad button on is selected then call true 
            else:
                rad_off.setChecked(True) # if the user chooses radio button off then call true

            def rad_change(): # new method called rad_change declared 
                if rad_on.isChecked(): # if statement to check if radio button is on
                    device.turn_on() # if selected then turns the device to on
                else:
                    device.turn_off() # if not , then turns device to off

            rad_on.toggled.connect(rad_change) # connects when button selected is changed 

        elif hasattr(device, 'write'): # if not a switch, check if it's a writeable device
            inp_value = QLineEdit() # inp_value var declared and edit widget assigned 
            inp_value.setText(str(device.read())) # inp_value var used and widget setText assigned as read

            btn_set = QPushButton('Set new value') # btn_set variable declared and QPushButton widget assigned and string set new value used

            def set_value(): # new method defined called set_value
                device.write(inp_value.text()) # gets the text value and reads the input 

            btn_set.clicked.connect(set_value) # btn_set method when clicked is connected and the set_value method is called to run

            layout.addWidget(inp_value) # method layout.addwidget is issued to invoke the inp_value var
            layout.addWidget(btn_set) # method layout.addwidget is issued to invoke the btn_set var

        elif hasattr(device, 'read'): # fixme
            lbl_value = QLabel(str(device.read())) # lbl_value var declared and QLabel widget is assigned as a string which invokes the device.read method
            layout.addWidget(lbl_value) # 

        panel.setLayout(layout)
        self.main_layout.addWidget(panel)



    def run(self):
        self.app.exec_()
