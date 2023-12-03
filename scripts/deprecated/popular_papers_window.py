
from pprint import pprint

import os
import sys
import json
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QRect, Qt, pyqtSignal

from clickable_label import ClickableLabel

class PopularPapersWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Set the background color
        self.setStyleSheet("background-color: #303030;")
        self.setGeometry(100, 100, 1200, 800)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        splitter = QSplitter(self)
        splitter.setStyleSheet("background-color: #303030;")

        # Left section with popular keywords
        left_widget = QWidget(splitter)
        left_layout = QVBoxLayout()

        popular_keywords_label = QLabel('Popular Keywords')
        popular_keywords_label.setStyleSheet("color: white; font-size: 18px; border-bottom: 1px solid white; font-weight: bold;")
        left_layout.addWidget(popular_keywords_label)

        subframe = QFrame(self)
        subframe.setFrameShape(QFrame.StyledPanel)
        subframe_layout = QVBoxLayout(subframe)

        keywords_list = [
            ('NLP', '130'),
            ('Computer Vision', '120'),
            ('NLP', '110'),
            ('ㅜㅜ', '190'),
            ('NLP', '130'),
            ('하...', '130'),
            ('NLP', '130'),
            ('살려줘', '130'),
            ('NLP', '130'),
            ('NLP', '130'),
            ('NLP', '130'),
        ]

        for i, keywords in enumerate(keywords_list):
            keyword_label = ClickableLabel(f"{i + 1}. {keywords[0]}")
            keyword_label.setStyleSheet("color: white;font-size: 16px;")
            keyword_label.linkActivated.connect(lambda _, keyword=keywords[0]: self.update_right_side(keyword))

            ref_label = QLabel(f"{keywords[1]} papers")
            ref_label.setStyleSheet("color: white;font-size: 12px;")

            item_layout = QHBoxLayout()
            item_layout.addWidget(keyword_label, alignment=Qt.AlignLeft)
            item_layout.addWidget(ref_label, alignment=Qt.AlignRight)

            subframe_layout.addLayout(item_layout)

        subframe_layout.addStretch()
        subframe.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(subframe)
        left_layout.addWidget(scroll_area)

        left_widget.setLayout(left_layout)


        # Right section with NLP title, order by label, and dropdown
        right_widget = QWidget(splitter)
        right_layout = QVBoxLayout()

        label_and_dropdown_layout = QHBoxLayout()

        self.popular_label = QLabel('')
        self.popular_label.setStyleSheet("color: white; font-size: 18px; border-bottom: 1px solid white; font-weight: bold;")
        label_and_dropdown_layout.addWidget(self.popular_label)

        # Add a QComboBox for dropdown
        self.order_by_dropdown = QComboBox(self)
        self.order_by_dropdown.addItems(["Title", "Author", "Keywords", "Reference", "Conference"])  # Add your options here
        self.order_by_dropdown.setStyleSheet("color: white; background-color: #303030;")
        self.order_by_dropdown.setFixedWidth(100)  # Set the desired width
        label_and_dropdown_layout.addWidget(self.order_by_dropdown)

        # Add the QHBoxLayout to the main QVBoxLayout
        right_layout.addLayout(label_and_dropdown_layout)

        self.order_by_dropdown.currentIndexChanged.connect(self.update_selected_option)

        # Related Papers 프레임
        paper_info = {
        'Paper Name': 'Sample Paper',
        'Author': 'John Doe',
        'Keywords': 'Sample, Keywords',
        'conf': 'IEEE',
        'Abstract': 'This is a sample abstract for the paper. ' * 10,  # 텍스트 길이 조절을 위해 반복
        'Related Papers': [
            {'Title': 'Related Paper 1', 'Author': 'Jane Doe', 'ref': 100, 'keywords': 'NLP, ML', 'conf': 'IEEE'},
            {'Title': 'Related Paper 2', 'Author': 'Bob Smith', 'ref': 10, 'keywords': 'NLP, ML', 'conf': 'IEEE'},
        ]
        }

        related_papers_frame = QFrame()
        subframe.setFrameShape(QFrame.StyledPanel)
        related_papers_layout = QVBoxLayout(related_papers_frame)
        related_papers_layout.setAlignment(Qt.AlignTop)  # 수직 정렬 추가

        for related_paper in paper_info['Related Papers']:
            paper_layout = QHBoxLayout()  # related paper 제목과 scrap 버튼을 수평으로 정렬하기 위한 레이아웃
            paper_title_label = ClickableLabel(f"{related_paper['Title']}")
            paper_title_label.setStyleSheet("color: white; font-size: 16px;")

            paper_author_label = ClickableLabel(f"Author: {related_paper['Author']}")
            paper_author_label.setStyleSheet("color: white; font-size: 12px;")

            paper_ref_label = ClickableLabel(f"Referenced: {related_paper['ref']}")
            paper_ref_label.setStyleSheet("color: white; font-size: 12px;")

            paper_keywords_label = ClickableLabel(f"Keywords: {related_paper['keywords']}")
            paper_keywords_label.setStyleSheet("color: white; font-size: 10px;")

            paper_conf_label = ClickableLabel(f"Published from: {related_paper['conf']}")
            paper_conf_label.setStyleSheet("color: white; font-size: 10px;")

            scrap_button = QPushButton("♥")
            scrap_button.setStyleSheet("border: none; color: white;")

            paper_layout.addWidget(paper_title_label)
            paper_layout.addWidget(paper_ref_label)
            paper_layout.addWidget(scrap_button, alignment=Qt.AlignRight)

            paper_separator = QFrame()
            paper_separator.setFrameShape(QFrame.HLine)
            paper_separator.setFrameShadow(QFrame.Sunken)

            # Connect scrap button click event
            scrap_button.clicked.connect(lambda _, title=related_paper['Title'], author=related_paper['Author']: self.scrap_paper(title, author))

            paper_title_label.linkActivated.connect(self.print_title)
            paper_author_label.linkActivated.connect(self.print_author)

            related_papers_layout.addLayout(paper_layout)
            related_papers_layout.addWidget(paper_author_label)
            related_papers_layout.addWidget(paper_keywords_label)
            related_papers_layout.addWidget(paper_conf_label)
            related_papers_layout.addWidget(paper_separator)

        # Related Papers 스크롤 영역
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(related_papers_frame)

        right_layout.addWidget(scroll_area)
        right_widget.setLayout(right_layout)

        # 합치기
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)

        splitter.setHandleWidth(1)
        splitter.setStyleSheet("QSplitter::handle{background: white;}")

        layout.addWidget(splitter)
        self.setLayout(layout)

    def update_right_side(self, keyword):
        print(f"Clicked Keyword: {keyword}")
        self.popular_label.setText(keyword)

    def scrap_paper(self, title, author):
        print(f"Scrapped Paper - Title: {title}, Author: {author}")
        
    def print_title(self, title):
        print(f"Clicked Title: {title}")

    def print_author(self, author):
        print(f"Clicked Author: {author}")

    def update_selected_option(self, index):
        selected_option = self.order_by_dropdown.currentText()
        print(f"Selected Option: {selected_option}")
