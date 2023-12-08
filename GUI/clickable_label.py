from PyQt5 import QtCore, QtGui, QtWidgets

class ClickableLabel(QtWidgets.QLabel):
    linkActivated = QtCore.pyqtSignal(str)

    def __init__(self, text):
        super().__init__(text)
        self.setTextInteractionFlags(QtCore.Qt.TextBrowserInteraction)
        self.setOpenExternalLinks(False)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.linkActivated.emit(self.text())
