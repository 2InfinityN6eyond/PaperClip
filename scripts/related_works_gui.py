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


class RelatedPaperGUI(QtWidgets.QDialog):
    def __init__(
        self,        
        paper
    ):
        super().__init__()

        self.paper = paper
        self.init_ui()

    def init_ui(self):
       
        '''
        # Paper Name 레이블
        paper_name_label = QtWidgets.QLabel(self.paper_info['Paper Name'])
        paper_name_label.setStyleSheet("color: white; font-size: 18px; border-bottom: 1px solid white; font-weight: bold;")

        # Author와 Keyword 레이블
        author_label = QtWidgets.QLabel(f"Author: {self.paper_info['Author']}")
        author_label.setStyleSheet("color: white; font-size: 12px;")
        keyword_label = QtWidgets.QLabel(f"Keywords: {self.paper_info['Keywords']}")
        keyword_label.setStyleSheet("color: white; font-size: 12px;")
        conf_label = QtWidgets.QLabel(f"Published from: {self.paper_info['conf']}")
        conf_label.setStyleSheet("color: white; font-size: 12px;")

        # Abstract 텍스트 에디터
        abstract_text = QTextEdit()
        abstract_text.setPlainText(self.paper_info['Abstract'])
        abstract_text.setReadOnly(True)
        abstract_text.setStyleSheet("color: white;")
        abstract_text.setFixedHeight(abstract_text.sizeHint().height())

        '''

        self.paper_meta_viewer = PaperMetaViewer(self.paper)

        # Related Work 레이블
        related_work_label = QtWidgets.QLabel("Related Work")
        related_work_label.setStyleSheet("color: white;font-size: 18px; border-bottom: 1px solid white; font-weight: bold;")

        related_works_scrollable = ScrollableList()
        related_works_scrollable.update(self.paper.reference_list)

        v_layout = QVBoxLayout()
        v_layout.addWidget(self.paper_meta_viewer)
        v_layout.addWidget(related_work_label)
        v_layout.addWidget(related_works_scrollable)


        return
    
        # Related Papers 프레임
        related_papers_frame = QFrame()
        related_papers_layout = QVBoxLayout(related_papers_frame)
        related_papers_layout.setAlignment(Qt.AlignTop)

        for related_paper in self.paper_info['Related Papers']:
            paper_layout = QHBoxLayout()

            paper_title_label = ClickableLabel(f"{related_paper['Title']}")
            paper_title_label.setStyleSheet("color: white; font-size: 16px;")
            paper_author_label = ClickableLabel(f"Author: {related_paper['Author']}")
            paper_author_label.setStyleSheet("color: white; font-size: 12px;")
            scrap_button = QPushButton("♥")
            scrap_button.setStyleSheet("border: none; color: white;")


            paper_layout.addWidget(paper_title_label)
            paper_layout.addWidget(scrap_button, alignment=Qt.AlignRight)

            paper_separator = QFrame()
            paper_separator.setFrameShape(QFrame.HLine)
            paper_separator.setFrameShadow(QFrame.Sunken)
            paper_separator.setStyleSheet("background: gray;")

            scrap_button.clicked.connect(lambda _, title=related_paper['Title'], author=related_paper['Author']: self.scrap_paper(title, author))

            paper_title_label.linkActivated.connect(self.open_related_paper_gui)
            paper_author_label.linkActivated.connect(self.print_author)

            related_papers_layout.addLayout(paper_layout)
            related_papers_layout.addWidget(paper_author_label)
            related_papers_layout.addWidget(paper_separator)

        # Related Papers 스크롤 영역
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(related_papers_frame)

        # 전체 레이아웃 구성
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(paper_name_label)
        main_layout.addWidget(author_label)
        main_layout.addWidget(keyword_label)
        main_layout.addWidget(conf_label)
        main_layout.addWidget(abstract_text)
        main_layout.addWidget(related_work_label)
        main_layout.addWidget(scroll_area)

        self.setWindowTitle(self.paper_info['Paper Name'])
        self.setStyleSheet("background-color: #303030;")
        self.setGeometry(200, 200, 800, 600)
        
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
