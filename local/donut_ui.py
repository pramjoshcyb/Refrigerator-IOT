from PyQt5.Qt import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import rpyc


class DonutUI():

    def __init__(self):

        self.app = QApplication([])

        connect_panel = self.create_connect_panel()

        window = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(connect_panel)
        window.setLayout(layout)
        window.show()


        self.main_layout = layout

        self.window = window

    def create_connect_panel(self):
        panel = QFrame()
        panel.setFrameShape(QFrame.Panel)
        layout = QVBoxLayout()
        lbl_ip_address = QLabel('Enter IP address or hostname:')
        inp_ip_address = QLineEdit()
        inp_ip_address.setText('127.0.0.2')
        btn_connect = QPushButton('Link new device')

        layout.addWidget(lbl_ip_address)
        layout.addWidget(inp_ip_address)
        layout.addWidget(btn_connect)

        def connect():
            hostname = inp_ip_address.text()
            connection = rpyc.classic.connect(hostname)
            device = connection.modules.__main__.my_device
            self.add_device_panel(device)

        btn_connect.clicked.connect(connect)

        panel.setLayout(layout)

        return panel

    def add_device_panel(self, device):
        panel = QFrame()
        panel.setFrameShape(QFrame.Box)
        layout = QVBoxLayout()

        lbl_name = QLabel('Device: ' + device.get_name())
        lbl_label = QLabel(device.get_label())

        layout.addWidget(lbl_name)
        layout.addWidget(lbl_label)
        if hasattr(device, 'turn_on'):
            rad_on = QRadioButton(device.get_on_label())
            rad_off = QRadioButton(device.get_off_label())
            layout.addWidget(rad_on)
            layout.addWidget(rad_off)

            if device.read() == True:
                rad_on.setChecked(True)
            else:
                rad_off.setChecked(True)

            def rad_change():
                if rad_on.isChecked():
                    device.turn_on()
                else:
                    device.turn_off()

            rad_on.toggled.connect(rad_change)

        elif hasattr(device, 'write'):
            inp_value = QLineEdit()
            inp_value.setText(str(device.read()))

            btn_set = QPushButton('Set new value')

            def set_value():
                device.write(inp_value.text())

            btn_set.clicked.connect(set_value)

            layout.addWidget(inp_value)
            layout.addWidget(btn_set)

        elif hasattr(device, 'read'):
            lbl_value = QLabel(str(device.read()))
            layout.addWidget(lbl_value)

        panel.setLayout(layout)
        self.main_layout.addWidget(panel)



    def run(self):
        self.app.exec_()
