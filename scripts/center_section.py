from pprint import pprint

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *

from containers import Paper
from scrollables import ScrollableList
from paper_item import PaperItem
from scrollable_label import ScrollableLabel
from popular_papers_window import PopularPapersWindow

from paper_clip_search_result_item import PaperClipSearchResultItem


class CenterSection(QtWidgets.QWidget) :
    def __init__(
        self,
        parent,
        query_handler
    ) :
        super().__init__()
        self.parent = parent
        self.query_handler = query_handler
        # Variable to store the selected item
        self.order_by = None
        
        most_popular_button = QtWidgets.QPushButton('View Popular Papers', self)
        most_popular_button.setStyleSheet("color: white; font-size: 18px; background-color: #505050;")
        most_popular_button.clicked.connect(self.view_most_popular_keywords)

        '''
        self.menu_function_map = {
            "Title" : self.query_handler.paperByTitle,
            #"DOI"   : lambda doi : self.query_handler.paperByDOI(doi, exact=True),
            "Author" : self.query_handler.paperByAuthor,
            "Keywords" : self.query_handler.paperByKeywords,
            "Conference" : self.query_handler.paperByConference,
        }
        '''
        self.menu_function_map = {
            "Title" : lambda title : self.query_handler.queryPaperBy(
                by = "p.title", value = title
            ),
            #"DOI" : lambda doi : self.query_handler.queryPaperBy(
            #    by = "p.DOI", value = doi
            #),
            "Author" : lambda author : self.query_handler.queryPaperBy(
                by = "apr.author_name", value = author
            ),
            "Conference" : lambda conference : self.query_handler.queryPaperBy(
                by = "p.journal", value = conference
            ),
            "Keywords" : lambda keywords : self.query_handler.queryPaperBy(
                by = "p.keywords", value = keywords
            ),
        }

        # Dropdown menu with five options
        self.dropdown_menu = QtWidgets.QComboBox(self)
        self.dropdown_menu.addItems(list(self.menu_function_map.keys()))
        self.dropdown_menu.setStyleSheet("color: white; background-color: #303030;")
        #self.dropdown_menu.currentIndexChanged.connect(self.update_order_by)

        self.search_input = QtWidgets.QLineEdit(self)
        self.search_input.setStyleSheet("color: white; background-color: #303030;")
        self.search_input.returnPressed.connect(self.search_button_clicked)

        self.search_button = QtWidgets.QPushButton('Search', self)
        self.search_button.setStyleSheet("color: black; background-color: white;")
        self.search_button.clicked.connect(self.search_button_clicked)

        search_layout = QtWidgets.QHBoxLayout()
        search_layout.addWidget(self.dropdown_menu)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_button)

        self.scrollable = ScrollableList(self)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(most_popular_button)
        layout.addLayout(search_layout)
        layout.addWidget(self.scrollable)
        self.setLayout(layout)
    
    def search_button_clicked(self):
        serach_input = self.search_input.text()
        dropdown_menu = self.dropdown_menu.currentText()
        search_result = self.menu_function_map[dropdown_menu](serach_input)

        print(len(search_result), "results found")
        item_list = []
        for paper in search_result :
            item = PaperClipSearchResultItem(self, paper)
            item_list.append(item)

        self.scrollable.update(item_list)


    def view_most_popular_keywords(self):
        popular_papers_window = PopularPapersWindow(
            parent=self,
            query_handler=self.query_handler
        )
        popular_papers_window.exec_()

    def itemClicked(self, paper) :
        self.parent.paperItemClicked(paper)

    def favorite_list_changed(self, item) :
        self.parent.favorite_list_changed(item)

    def favorite_list_changed_from_outside(self, item) :
        self.scrollable.favorite_list_changed_from_outside(item)