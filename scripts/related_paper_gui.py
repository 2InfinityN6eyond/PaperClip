from pprint import pprint

from PyQt5 import QtCore, QtGui, QtWidgets 

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
#import mysql.connector

from containers import Paper
from scrollables import ScrollableList
from clickable_label import ClickableLabel
from paper_meta_viewer import PaperMetaViewer
from paper_item import PaperItem

class RelatedPaperGUI(QtWidgets.QDialog):
    def __init__(
        self,
        parent,
        paper
    ):
        super().__init__()
        self.parent = parent
        self.paper = paper
        self.init_ui()
        self.setStyleSheet("background-color: #303030;")

    def init_ui(self):

        self.paper_meta_viewer = PaperMetaViewer(self.paper)
        self.paper_meta_viewer.show()
        self.paper_meta_viewer.setStyleSheet("background-color: #303030;")

        # Related Work 레이블
        related_work_label = QtWidgets.QLabel("Related Work")
        related_work_label.setStyleSheet("color: white;font-size: 18px; border-bottom: 1px solid white; font-weight: bold;")

        self.related_works_scrollable = ScrollableList(self)

        v_layout = QVBoxLayout(self)
        related_work_label.setStyleSheet("color: white; background-color: #303030;")
        v_layout.addWidget(self.paper_meta_viewer)
        v_layout.addWidget(related_work_label)
        v_layout.addWidget(self.related_works_scrollable)
        # v_layout.setStyleSheet("color: white; background-color: #303030;")

        self.update(self.paper)




    def update(self, paper):
        self.paper = paper
        self.paper_meta_viewer.update(self.paper)

        paper_item_list = []
        if self.paper is None or self.paper.reference_list is None:
            return
        
        for ref in self.paper.reference_paper_list:
            paper_item = PaperItem(self.related_works_scrollable, ref)
            paper_item_list.append(paper_item)

        self.related_works_scrollable.update(paper_item_list)


    def itemClicked(self, item) :
        print("item clicked")

        related_paper_gui = RelatedPaperGUI(self, item)
        related_paper_gui.exec_()

        
    def open_related_paper_gui(self, title):
        related_paper_info = self.get_related_paper_info(title)  # title을 통해 관련 논문 정보 가져오기

        # 새로운 GUI를 띄우기 위한 RelatedPaperGUI 인스턴스 생성
        related_paper_gui = RelatedPaperGUI(related_paper_info)
        related_paper_gui.exec_()
    
    def get_related_paper_info(self, title):
        # title을 이용하여 관련 논문의 정보를 가져오는 함수 (실제로는 데이터베이스 조회 등이 필요)
        # 여기서는 간단한 예시로 더미 데이터를 반환
        return {
            'GUI' : '1010101',
            'Paper Name': f'{title}',
            'Author': 'Unknown Author',
            'conf': 'IEEE',
            'Keywords': 'Related, Keywords',
            'Abstract': 'This is the abstract for the related paper.',
            'Related Papers': [{'Title': 'Related Paper 1', 'Author': 'Jane Doe', 'ref': 100, 'keywords': 'NLP, ML', 'conf': 'IEEE',},
            {'Title': 'Related Paper 2', 'Author': 'Bob Smith', 'ref': 10, 'keywords': 'NLP, ML', 'conf': 'IEEE',},]
        }
        
    def scrap_paper(self, title, author):
        print(f"Scrapped Paper - Title: {title}, Author: {author}")
        
    def print_title(self, title):
        print(f"Clicked Title: {title}")

    def print_author(self, author):
        print(f"Clicked Author: {author}")

    def favorite_list_changed(self, item):
        self.parent.favorite_list_changed(item)