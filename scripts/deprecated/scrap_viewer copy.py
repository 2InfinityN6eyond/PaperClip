from PyQt5 import QtCore, QtGui, QtWidgets
import qtawesome as qta

from scrollables import ScrollableList

class ScrapItem_(QtWidgets.QLabel):
    def __init__(
        self,
        parent,
        title,
        author,
        is_in_favorite=False,
        button_icon_width=50,
        button_icon_height=50,
    ):
        #super(ScrapItem, self).__init__(parent=parent)
        super().__init__(parent=parent)
        self.setStyleSheet("background-color: #303030; border-bottom: 1px solid white;")
        
        #self.mousePressEvent = self.itemClicked

        self.parent = parent
        self.is_in_favorite = is_in_favorite

        self.title_label = QtWidgets.QLabel(title)
        self.title_label.setStyleSheet("""
            QLabel {
                background-color: #303030;
                border-style: none;
            }
        """)

        self.author_label = QtWidgets.QLabel(author)
        #self.author_label.clicked.connect(self.authorClicked)
        #self.author_label.mousePressEvent = self.authorClicked

        self.heartButton = QtWidgets.QPushButton()
        self.heartButton.setStyleSheet("""
            QPushButton {
                background-color: #303030;
                border-style: none;
            }
        """)
        self.heartButton.setFixedSize(QtCore.QSize(button_icon_width, button_icon_height))

        self.false_icon = qta.icon('ph.paperclip-horizontal-thin', color='grey', options=[{'font-size': '40pt'}])
        self.true_icon  = qta.icon('ph.paperclip-horizontal-thin', color='white', options=[{'font-size': '40pt'}])

        self.heartButton.setIcon(self.false_icon)
        self.heartButton.setIconSize(self.false_icon.actualSize(self.heartButton.size()))
        self.heartButton.clicked.connect(self.toggleHeart)

        self.h_layout = QtWidgets.QHBoxLayout()
        self.h_layout.addWidget(self.title_label)
        self.h_layout.addWidget(self.heartButton) 
        title_and_button_widget = QtWidgets.QWidget()
        title_and_button_widget.setLayout(self.h_layout)

        self.v_layout = QtWidgets.QVBoxLayout()
        self.v_layout.addWidget(title_and_button_widget)
        self.v_layout.addWidget(self.author_label)
        self.setLayout(self.v_layout)
    
    def itemClicked(self, event):
        print("item clicked")
        self.parent.itemClicked(self)

    def toggleHeart(self):
        self.is_in_favorite = not self.is_in_favorite
        if self.is_in_favorite:
            print("wtf")
            self.heartButton.setIcon(self.true_icon)
        else:
            self.heartButton.setIcon(self.false_icon)    

    def authorClicked(self):
        print("author clicked")



class ScrapItem(QtWidgets.QWidget):
    def __init__(
            self,
            parent,
            title,
            author,
            is_in_favorite=False,
        ):
        super().__init__(parent=parent)
        self.setStyleSheet("background-color: #303030; border-bottom: 1px solid white;")
        
        self.parent = parent
        self.is_in_favorite = is_in_favorite


        title_label = QtWidgets.QLabel(title)
        title_label.setStyleSheet("""
            QLabel {
                background-color: #303030;
                border-style: none;
            }
        """)

        self.author_label = QtWidgets.QLabel(author)
        #self.author_label.clicked.connect(self.authorClicked)

        self.heartButton = QtWidgets.QPushButton()
        self.heartButton.setStyleSheet("""
            QPushButton {
                background-color: #303030;
                border-style: none;
            }
        """)
        self.heartButton.setFixedSize(QtCore.QSize(50, 50))

        self.false_icon = qta.icon('ph.paperclip-horizontal-thin', color='grey', options=[{'font-size': '40pt'}])
        self.true_icon  = qta.icon('ph.paperclip-horizontal-thin', color='white', options=[{'font-size': '40pt'}])

        self.heartButton.setIcon(self.false_icon)
        self.heartButton.setIconSize(self.false_icon.actualSize(self.heartButton.size()))
        self.heartButton.clicked.connect(self.toggleHeart)

        h_layout = QtWidgets.QHBoxLayout()
        h_layout.addWidget(title_label)
        h_layout.addWidget(self.heartButton)
        title_and_button_widget = QtWidgets.QWidget()
        title_and_button_widget.setLayout(h_layout)

        v_layout = QtWidgets.QVBoxLayout()
        v_layout.addWidget(title_and_button_widget)
        v_layout.addWidget(self.author_label)

        self.setLayout(v_layout)

        return
        self.layout = QtWidgets.QHBoxLayout()
        self.layout.addWidget(title_label)
        self.layout.addWidget(self.heartButton)
        self.setLayout(self.layout)

    def toggleHeart(self):
        self.is_in_favorite = not self.is_in_favorite
        if self.is_in_favorite:
            print("wtf")
            self.heartButton.setIcon(self.true_icon)
        else:
            self.heartButton.setIcon(self.false_icon)



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