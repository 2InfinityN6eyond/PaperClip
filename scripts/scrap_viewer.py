from PyQt5 import QtCore, QtGui, QtWidgets
import qtawesome as qta

from scrollables import ScrollableList
from scrap_item import ScrapItem


class ScrapViewer(QtWidgets.QFrame):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        scrap_label = QtWidgets.QLabel("CLIPS")
        scrap_label.setStyleSheet("color: white; font-size: 18px; border-bottom: 1px solid white; font-weight: bold;")

        self.scrollable = ScrollableList()

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(scrap_label)
        layout.addWidget(self.scrollable)
        self.setLayout(layout)
        
        self.updateSample()


    def update(self, item_list) :
        for item in item_list :
            self.scrollable.scrollAreaLayout.addWidget(item)

    def itemClicked(self, item):
        print("item clicked")


    def updateSample(self) :
        item_list = []
        for i in range(10):
            item = ScrapItem(self, f"제목 {i+1}", "작가")
            item_list.append(item)
        self.update(item_list)