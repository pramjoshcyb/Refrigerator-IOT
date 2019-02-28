from PyQt5.Qt import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

SPACING_AMOUNT = 25

# adapted from Draggable Text Example in Qt 5 documentation
# https://doc.qt.io/qt-5/qtwidgets-draganddrop-draggabletext-dragwidget-cpp.html

class DragDropContainer(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.setAcceptDrops(True)

    def add_child(self, widget):
        """adds a widget to the bottom of the drag'n'drop container"""
        self.layout.addWidget(widget)

    def mousePressEvent(self, event):
        """called when the drag begins (the mouse button is pushed down)"""

        # we need to find the widget that the mouse is on

        i = 0
        mouse_coords = event.pos()
        while i < self.layout.count() and mouse_coords.y() >= self.layout.itemAt(i).widget().y():
            i += 1
        i -= 1
        if i < 0:
            i = 0
        if i >= self.layout.count():
            return

        # `i` now contains the position of the widget in the sequence



        # we put the position into the mime descriptor for later retrieval

        mimeData = QMimeData()
        mimeData.setText(str(i))


        # now get the actual widget itself
        child = self.layout.itemAt(i).widget()

        # make the dragged item follow the cursor properly
        hotspot = event.pos() - child.pos()

        # insert spacers
        self.drag_begin()


        ###########################
        #                         #
        # drag'n'drop boilerplate #
        #                         #

        dpr = self.window().windowHandle().devicePixelRatio()
        pixmap = QPixmap(child.size() * dpr)
        pixmap.setDevicePixelRatio(dpr)
        child.render(pixmap)

        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setPixmap(pixmap)
        drag.setHotSpot(hotspot)

        dropAction = drag.exec(Qt.CopyAction | Qt.MoveAction, Qt.CopyAction)
        #                         #
        #                         #
        ###########################


    def dragEnterEvent(self, event):
        """called to make sure drop events are accepted in this container"""

        ###########################
        #                         #
        # drag'n'drop boilerplate #
        #                         #
        if event.mimeData().hasText():
            if event.source() == self:
                event.setDropAction(Qt.MoveAction)
                event.accept()
            else:
                event.acceptProposedAction()
        else:
            event.ignore()
        #                         #
        #                         #
        ###########################

    def dropEvent(self, event):
        """called whan any dragged item is dropped onto the container"""
        mime = event.mimeData()

        # if we are receiving the right sort of event
        if mime.hasText():

            # we put the position into the mime descriptor earlier
            old_pos = int(str(mime.text()))
            click_y = event.pos().y()

            # remember that we have created the spacers between widgets
            # so skip every second item in the layout
            i = 1
            # stop when the mouse position is beyond the top of a widget
            while ( i < self.layout.count() and
                      click_y >= self.layout.itemAt(i).widget().y() ):
                i += 2
            # convert the doubled position to the normal position
            new_pos = i // 2

            widget = self.layout.itemAt(old_pos * 2 + 1).widget()
            # get rid of spacers
            self.drag_done()

            # remove the widget from the flow
            self.layout.removeWidget(widget)

            # this fixes the situation when the deleted widget changes the
            # positions of later widgets
            if new_pos > old_pos:
                new_pos -= 1

            # put the widget back into the layout in the new position
            self.layout.insertWidget(new_pos, widget)

        ###########################
        #                         #
        # drag'n'drop boilerplate #
        #                         #
            if event.source() == self:
                event.setDropAction(Qt.MoveAction)
                event.accept()
            else:
                event.acceptProposedAction()
        else:
            event.ignore()
        #                         #
        #                         #
        ###########################

    def drag_begin(self):
        """add spacers between widgets"""
        i = self.layout.count()
        while i >= 0:
            self.layout.insertSpacing(i, SPACING_AMOUNT)
            i -= 1
        # shrink the container after spacers removed
        self.updateGeometry()
        self.adjustSize()

    def drag_done(self):
        """remove spacers between widgets"""
        i = 0
        while i < self.layout.count():
            self.layout.removeItem(self.layout.itemAt(i))
            i += 1
        # shrink the container after spacers removed
        self.updateGeometry()
        self.adjustSize()

    def list_widgets(self):
        """returns a list of the widgets in display order"""
        return [self.layout.itemAt(i).widget() for i in range(self.layout.count())]
