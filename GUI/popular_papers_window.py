
from pprint import pprint

import os
import sys
import json
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QRect, Qt, pyqtSignal

from clickable_label import ClickableLabel
from scrollables import ScrollableList

from paper_clip_search_result_item import PaperClipSearchResultItem


class PaperWithCountItem(QWidget) :
    def __init__(
        self,
        parent,
        idx,
        keyword,
        count
    ) :
        super().__init__()
        self.setStyleSheet("background-color: #303030;")
        self.mousePressEvent = self.itemClicked

        self.parent = parent
        self.idx = idx
        self.keyword = keyword
        self.count = count

        self.keyword_label = QLabel(f"{self.idx+1}. {self.keyword}")
        self.keyword_label.setStyleSheet("color: white;font-size: 16px;")
        self.keyword_label.linkActivated.connect(lambda _, keyword=self.keyword: self.update_right_side(keyword))

        self.count_label = QLabel(f"{self.count} papers")
        self.count_label.setStyleSheet("color: white;font-size: 12px;")

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.keyword_label, alignment=Qt.AlignLeft)
        self.layout.addWidget(self.count_label, alignment=Qt.AlignRight)

        self.setLayout(self.layout)

    def itemClicked(self, event):
        print(f"Clicked {self.keyword}")
        self.parent.update_right_side(self.keyword)

class PopularPapersWindow(QDialog):
    def __init__(
        self,
        parent,
        query_handler
    ):
        super().__init__(parent)
        self.query_handler = query_handler
        self.parent = parent

        # Set tthe background color
        self.setStyleSheet("background-color: #303030;")
        self.setGeometry(100, 100, 1200, 800)
        

        popular_keywords_label = QLabel('Popular Keywords')
        popular_keywords_label.setStyleSheet("color: white; font-size: 18px; border-bottom: 1px solid white; font-weight: bold;")
        
        self.paper_keyword_scrollable_list = ScrollableList(self)

        left_layout = QVBoxLayout()
        left_layout.addWidget(popular_keywords_label)
        left_layout.addWidget(self.paper_keyword_scrollable_list)

        left_widget = QWidget()
        left_widget.setLayout(left_layout)


        self.placeholder_label = QLabel('')
        self.placeholder_label.setStyleSheet("color: white; font-size: 18px; border-bottom: 1px solid white; font-weight: bold;")

        self.paper_scrollable_list = ScrollableList(self)

        right_layout = QVBoxLayout()
        right_layout.addWidget(self.placeholder_label)
        right_layout.addWidget(self.paper_scrollable_list)

        right_widget = QWidget()
        right_widget.setLayout(right_layout)


        splitter = QSplitter(self)
        splitter.setStyleSheet("background-color: #303030;")
        splitter.setStyleSheet("QSplitter::handle{background: white;}")
        splitter.setHandleWidth(1)
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(splitter)
        self.setLayout(layout)

        self.updateKeywordList()

    def updateKeywordList(self):
        keyword_count_list = self.query_handler.fetchTopKeywords()
        item_list = []
        for i, (keyword, count) in enumerate(keyword_count_list) :
            print(keyword, count)
            item = PaperWithCountItem(
                parent  = self,
                idx     = i,
                keyword = keyword,
                count   = count
            )
            item_list.append(item)
        print(len(item_list))
        self.paper_keyword_scrollable_list.update(item_list)
        
        print(self.paper_keyword_scrollable_list.scrollAreaLayout.count())

    def update_right_side(self, keyword):
        self.placeholder_label.setText(f"{keyword}")
        paper_list = self.query_handler.queryPaperBy(
            by="p.keywords", value=keyword
        )
        item_list = []
        for i, paper in enumerate(paper_list) :
            item = PaperClipSearchResultItem(
                parent  = self,
                paper   = paper
            )
            item_list.append(item)
        self.paper_scrollable_list.update(item_list)

    def itemClicked(self, item):
        print("item clicked")

    def favorite_list_changed(self, item):
        self.parent.favorite_list_changed(item)