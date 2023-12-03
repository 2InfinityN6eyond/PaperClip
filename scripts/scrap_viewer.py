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

        #subframe = QtWidgets.QFrame(self)
        #subframe.setFrameShape(QtWidgets.QFrame.StyledPanel)
        #Msubframe_layout = QtWidgets.QVBoxLayout(subframe)

        self.scrollable = ScrollableList()
        

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(scrap_label)
        layout.addWidget(self.scrollable)
        self.setLayout(layout)
        

        '''
        for i in range(10):
            title_label = QtWidgets.QLabel(f"제목 {i+1}")
            title_label.setStyleSheet("color: white;")

            scrap_button = QtWidgets.QPushButton("\U0001F4CE") #clip
            scrap_button.setStyleSheet("border: none; color: white;")

            scrap_button.clicked.connect(lambda _, title=f"제목 {i+1}": print(title))

            item_layout = QtWidgets.QHBoxLayout()
            item_layout.addWidget(title_label, alignment=Qt.AlignLeft)
            item_layout.addWidget(scrap_button, alignment=Qt.AlignRight)

            subframe_layout.addLayout(item_layout)
        '''

        #subframe_layout.addStretch()
        #[subframe].setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        #scroll_area = QtWidgets.QScrollArea(self)
        #scroll_area.setWidgetResizable(True)
        #scroll_area.setWidget(subframe)

        #layout.addWidget(scroll_area)

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