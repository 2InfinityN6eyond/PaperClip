from PyQt5 import QtWidgets, QtCore

class ScrollableLabel(QtWidgets.QWidget):
    def __init__(self, text=None, style_sheet = None):
        super().__init__()
        self.style_sheet = style_sheet
        self.initUI(text)

    def initUI(self, text):
        
        # Create a QLabel with long text
        self.label = QtWidgets.QLabel(text, self)
        if self.style_sheet :
            self.label.setStyleSheet(self.style_sheet)
        self.label.setWordWrap(False)  # Disable word wrap

        # Create a QScrollArea
        self.scrollArea = QtWidgets.QScrollArea(self)
        self.scrollArea.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum
        )
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.label)
        #self.scrollArea.setFixedHeight(50)
        self.scrollArea.setAlignment(QtCore.Qt.AlignTop)


        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.scrollArea)
        self.setLayout(layout)

    def setText(self, text) :
        self.label.setText(text)
    def setStyleSheet(self, style_sheet: str | None) -> None:
        self.label.setStyleSheet(style_sheet)

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    long_text = "This is a very long text that will not fit in a regular label, so it needs to be scrollable."
    demo = ScrollableLabel(long_text)
    demo.show()
    sys.exit(app.exec_())
