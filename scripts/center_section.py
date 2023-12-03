from pprint import pprint

from PyQt5 import QtWidgets, QtCore, QtGui

from containers import Paper
from scrollables import ScrollableList
from paper_item import PaperItem
from scrollable_label import ScrollableLabel

class PaperClipSearchResultItem(QtWidgets.QWidget) :
    def __init__(
        self,
        parent,
        paper: Paper,
        true_icon = "\U0001F4CE",
        false_icon = "\U0001F4C1"
    ) :

        super().__init__(parent=parent)
        self.mousePressEvent = self.itemClicked

        self.parent = parent
        self.paper = paper

        if (
            self.paper is not None
        ) and (
            self.paper.title is None
        ) and (
            self.paper.DOI is not None
        ) :
            self.paper.title = self.paper.DOI

        self.true_icon_str  = true_icon
        self.false_icon_str = false_icon

        self.initUI()
        self.update()

    def initUI(self) :
        #self.title_label = QtWidgets.QLabel()
        self.title_label = ScrollableLabel()
        self.title_label.setStyleSheet("color: white; font-size: 16px;")

        self.scrap_button = QtWidgets.QPushButton(
            self.true_icon_str if self.paper.is_in_favorite else self.false_icon_str,
        ) #folder
        self.scrap_button.clicked.connect(self.favorite_list_changed)
        self.scrap_button.setStyleSheet("border: none; color: white;")

        title_button_layout = QtWidgets.QHBoxLayout()
        title_button_layout.addWidget(self.title_label)
        title_button_layout.addWidget(self.scrap_button, alignment=QtCore.Qt.AlignRight)

        #self.author_label = QtWidgets.QLabel()
        self.author_label = ScrollableLabel()
        self.author_label.setStyleSheet("color: white; font-size: 12px;")
        
        #self.keyward_label = QtWidgets.QLabel()
        self.keyword_label = ScrollableLabel()
        self.keyword_label.setStyleSheet("color: white; font-size: 10px;")

        #self.conf_label = QtWidgets.QLabel()
        self.conf_label = ScrollableLabel()
        self.ref_count_label = QtWidgets.QLabel()

        conf_ref_count_layout = QtWidgets.QHBoxLayout()
        conf_ref_count_layout.addWidget(self.conf_label)
        conf_ref_count_layout.addWidget(self.ref_count_label, alignment=QtCore.Qt.AlignRight)

        paper_layout = QtWidgets.QVBoxLayout(self)
        paper_layout.addLayout(title_button_layout)
        paper_layout.addWidget(self.author_label)
        paper_layout.addWidget(self.keyword_label)
        paper_layout.addLayout(conf_ref_count_layout)

    def update(self) :
        if self.paper is None :
            return

        if self.paper.title is not None :
            self.title_label.setText(self.paper.title)
        else :
            self.title_label.setText("NULL")
        
        if self.paper.authors is not None :
            author_text = ", ".join(self.paper.authors)


            self.author_label.setText(author_text)
        else :
            self.author_label.setText("NULL")
        
        #if self.paper.keyword_list is not None :
            
        if self.paper.conference_acronym is not None :
            self.conf_label.setText(self.paper.conference_acronym)
        else :
            self.conf_label.setText("NULL")

        if self.paper.reference_count is not None :
            self.ref_count_label.setText(str(self.paper.reference_count))
        else :
            self.ref_count_label.setText("NULL")

    def itemClicked(self, event) :
        print("item clicked")
        self.parent.itemClicked(self.paper)

    def toggleHeart(self) :
        self.scrap_button.setText(
            self.true_icon_str if self.paper.is_in_favorite else self.false_icon_str
        )

    def favorite_list_changed(self) :
        if self.paper.authors is None :
            return
        self.paper.toggleFavorite()
        self.toggleHeart()
        self.parent.favorite_list_changed(self.paper)


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

    def view_most_popular_keywords(self):
        pass
        #self.parent().view_most_popular_keywords()
    
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

    def itemClicked(self, paper) :
        self.parent.paperItemClicked(paper)

    def favorite_list_changed(self, item) :
        self.parent.favorite_list_changed(item)

    def favorite_list_changed_from_outside(self, item) :
        self.scrollable.favorite_list_changed_from_outside(item)