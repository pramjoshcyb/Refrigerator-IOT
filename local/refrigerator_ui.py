from PyQt5.Qt import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from drag_drop_container import *

import rpyc # importing remote procedure call


class RefrigeratorUI(QWidget): # creating a class called RefrigeratorUI 
                # init is a reserved method in python classes, called when an object is created from the class
    def __init__(self): # self represents instance of class RefrigeratorUI, which allows to access attributes and methods of class
        """initialises the method and assigns hostname"""
        self.app = QApplication([]) # initialises the window and constructs an app object
        # instance of the class attribute where app is a local var
        connect_panel = self.create_connect_panel() # creating a var called connect_panel and the attribute self.create_connect_panel of the QFrame type is being assigned

        connect_panel.hostname = None # something here relates to hint 2 and you got it!
        dd_container = DragDropContainer() # variable that the instance of the DragDropContainer class is being added to
        dd_container.add_child(connect_panel) # using the method dd_container.add_child to add the widget 

        # this creates a main window out of the container
        dd_container.show()
        self.dd_container = dd_container

        hostname_file = 'hostname.txt'
        with open(hostname_file) as file_object:
            readlines = file_object.readlines() 
            for line in readlines:
                hostname = line.strip()
                connection = rpyc.classic.connect(hostname)
                device = connection.modules.__main__.my_device
                self.add_device_panel(device, hostname)
            print(readlines)


        #for lineread in readlines:

        # for readfile in add_device_panel:


    def create_connect_panel(self): # method for create_connect_panel
        """Creates a panel (a QFrame widget), puts content into it appropriate for
        the connection panel, and returns the panel"""
        # self.create_connect_panel()
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
        


        def connect(): # new method connect #SET HOSTNAME TO NONE HERE?
            hostname = inp_ip_address.text() # declared hostname var and assigned the input of ip address to it
            connection = rpyc.classic.connect(hostname) # declared connection var and assigned the remote call to connect to the host
            device = connection.modules.__main__.my_device # declared device var and assigned the conn module to it 
            self.add_device_panel(device, hostname) # self method to access attribute of the device 

        btn_connect.clicked.connect(connect) # when the link new device btn is clicked it connects to server

        panel.setLayout(layout) # calls layout method to set the panel

        return panel # returns the panel 

    def add_device_panel(self, device, hostname): # new method that takes parameters self and device 
        panel = QFrame() # initiates the QFrame widget assigned to the panel of the GUI
        panel.setFrameShape(QFrame.Box) # panel method to set the frame shape in rectangle
        layout = QVBoxLayout()
        panel.hostname = hostname
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
        self.dd_container.add_child(panel) # self attribute to call the container and add the widget of the QFrame type



    def run(self):
        self.app.exec_()

        #app quitting
        hostname_file = 'hostname.txt'
        with open(hostname_file, 'w') as file_object:
            for widget in self.dd_container.list_widgets(): # receives panels
                print(widget.hostname) # once terminal is closed it should print out the hostnames, try to figure it out and then write to file
                if widget.hostname is not None:
                    file_object.write(widget.hostname+'\n')
        
                

                    
