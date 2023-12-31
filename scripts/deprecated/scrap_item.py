from PyQt5 import QtWidgets, QtCore
import qtawesome as qta

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
        self.mousePressEvent = self.itemClicked
        
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
        self.author_label.mousePressEvent = self.authorClicked

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
        h_layout.addWidget(self.title_label)
        h_layout.addWidget(self.heartButton)
        title_and_button_widget = QtWidgets.QWidget()
        title_and_button_widget.setLayout(h_layout)

        v_layout = QtWidgets.QVBoxLayout()
        v_layout.addWidget(title_and_button_widget)
        v_layout.addWidget(self.author_label)

        self.setLayout(v_layout)

    def itemClicked(self, event):
        print("item clicked")
        self.parent.itemClicked(self)

    def authorClicked(self, event):
        print("author clicked")


    def toggleHeart(self):
        self.is_in_favorite = not self.is_in_favorite
        if self.is_in_favorite:
            print("wtf")
            self.heartButton.setIcon(self.true_icon)
        else:
            self.heartButton.setIcon(self.false_icon)
