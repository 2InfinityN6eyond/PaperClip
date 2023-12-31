import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QScrollArea
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QPixmap

import qtawesome as qta
from PyQt5 import QtCore, QtGui, QtWidgets


class ListItem(QWidget):
    def __init__(
            self,
            text,
            is_in_favorite=False,
        ):
        super().__init__()
        self.setStyleSheet("background-color: #303030; border-bottom: 1px solid white;")

        self.is_in_favorite = is_in_favorite

        self.layout = QtWidgets.QHBoxLayout()

        self.label = QLabel(text)
        self.label.setStyleSheet("""
            QLabel {
                background-color: #303030;
                border-style: none;
            }
        """)
        self.heartButton = QPushButton()
        self.heartButton.setStyleSheet("""
            QPushButton {
                background-color: #303030;
                border-style: none;
            }
        """)
        self.heartButton.setFixedSize(QSize(50, 50))

        self.false_icon = qta.icon('ph.paperclip-horizontal-thin', color='grey', options=[{'font-size': '40pt'}])
        self.true_icon  = qta.icon('ph.paperclip-horizontal-thin', color='white', options=[{'font-size': '40pt'}])

        self.heartButton.setIcon(self.false_icon)
        self.heartButton.setIconSize(self.false_icon.actualSize(self.heartButton.size()))
        self.heartButton.clicked.connect(self.toggleHeart)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.heartButton)
        self.setLayout(self.layout)

    def toggleHeart(self):
        self.is_in_favorite = not self.is_in_favorite
        if self.is_in_favorite:
            print("wtf")
            self.heartButton.setIcon(self.true_icon)
        else:
            self.heartButton.setIcon(self.false_icon)

class SrollableList(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #303030;")

        self.layout = QVBoxLayout()
        self.scrollArea = QScrollArea()
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaLayout = QVBoxLayout(self.scrollAreaWidgetContents)

        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.layout.addWidget(self.scrollArea)
        self.setLayout(self.layout)

    def update(self, item_list) :
        for item in item_list :
            self.scrollAreaLayout.addWidget(item)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    #mainWindow = MainWindow()
    mainWindow = SrollableList()

    item_list = []
    for i in range(10):
        item_list.append(ListItem(f"제목 {i+1}"))
    mainWindow.update(item_list)
    mainWindow.show()
    sys.exit(app.exec_())
