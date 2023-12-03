from PyQt5 import QtCore, QtGui, QtWidgets 

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
#import mysql.connector

from containers import Paper, Author
from scrollable_label import ScrollableLabel

class PaperMetaViewer(QtWidgets.QLabel):
    def __init__(self, paper: Paper):
        super().__init__()
        self.paper = paper
        self.initUI()

    def initUI(self):

        # Paper Name 레이블
        #self.paper_name_label = QtWidgets.QLabel()
        self.paper_name_label = ScrollableLabel()
        self.paper_name_label.setStyleSheet("color: white; font-size: 18px; border-bottom: 1px solid white; font-weight: bold;")

        # Author와 Keyword 레이블
        #self.author_label = QtWidgets.QLabel() #(", ".join(author_name_list))
        self.author_label = ScrollableLabel()
        self.author_label.setStyleSheet("color: white; font-size: 12px;")
        #keyword_label = QtWidgets.QLabel(f"Keywords: {self.paper_info['Keywords']}")
        #keyword_label.setStyleSheet("color: white; font-size: 12px;")
        self.conf_label = QtWidgets.QLabel() #(f"Published from: {self.paper.conference}")
        self.conf_label.setStyleSheet("color: white; font-size: 12px;")

        # Abstract 텍스트 에디터
        self.abstract_text = QTextEdit()
        self.abstract_text.setPlainText("--------------") #(self.paper.abstract)
        self.abstract_text.setReadOnly(True)
        self.abstract_text.setStyleSheet("color: white;")
        self.abstract_text.setFixedHeight(self.abstract_text.sizeHint().height())

        #self.setText(self.paper.title)
        #self.setStyleSheet("color: white; font-size: 18px; border-bottom: 1px solid white; font-weight: bold;")
        #self.setWordWrap(True)
        #self.setFixedHeight(self.sizeHint().height())

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.paper_name_label)
        main_layout.addWidget(self.author_label)
        #main_layout.addWidget(keyword_label)
        main_layout.addWidget(self.conf_label)
        main_layout.addWidget(self.abstract_text)

        self.update(self.paper)

    def update(self, paper):
        self.paper = paper
        if paper is None :
            return

        title = self.paper.title
        author_list : list[Author] = self.paper.author_list
        author_name_list = list(map(lambda author: author.name, author_list))
        conference = self.paper.conference_acronym
        abstract = self.paper.abstract_text

        self.paper_name_label.setText(title)
        self.author_label.setText(", ".join(author_name_list))
        self.conf_label.setText(f"Published from: {conference}")
        self.abstract_text.setPlainText(abstract)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.linkActivated.emit(self.text())
