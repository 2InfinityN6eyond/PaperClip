from pprint import pprint

from PyQt5 import QtCore, QtGui, QtWidgets

from scrollables import ScrollableList
from paper_item import PaperItem

class ScrapViewer(QtWidgets.QFrame):
    def __init__(
        self,
        parent=None,
    ):
        super().__init__(parent=parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        scrap_label = QtWidgets.QLabel("CLIPS")
        scrap_label.setStyleSheet("color: white; font-size: 18px; border-bottom: 1px solid white; font-weight: bold;")

        self.scrollable = ScrollableList(self)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(scrap_label)
        layout.addWidget(self.scrollable)
        self.setLayout(layout)
        
    def update(self, item_list) :
        for item in item_list :
            paper_item = PaperItem(self, item)
            self.scrollable.scrollAreaLayout.addWidget(paper_item)

    def append(self, item) :
        paper_item = PaperItem(self, item)
        self.scrollable.scrollAreaLayout.addWidget(paper_item)

    def remove(self, item) :
        for i in reversed(range(self.scrollable.scrollAreaLayout.count())) :
            if self.scrollable.scrollAreaLayout.itemAt(i).widget().paper.DOI == item.DOI :
                self.scrollable.scrollAreaLayout.itemAt(i).widget().setParent(None)
                break

    def itemClicked(self, item):
        self.parent.paperItemClicked(item)


    def favorite_list_changed(self, item):
        self.parent.favorite_list_changed(item)