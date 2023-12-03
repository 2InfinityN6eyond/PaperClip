from PyQt5 import QtWidgets, QtCore, QtGui

from containers import Paper
from scrollables import ScrollableList
from paper_item import PaperItem

class PaperClipSearchResultItem(QtWidgets.QWidget) :
    def __init__(
        self,
        parent,
        paper: Paper
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

        self.true_icon_str = "\U00002713"
        self.false_icon_str = "\U0000274C"

        self.initUI()
        self.update()

    def initUI(self) :
        self.title_label = QtWidgets.QLabel()
        self.title_label.setStyleSheet("color: white; font-size: 16px;")

        self.scrap_button = QtWidgets.QPushButton(self.true_icon_str) #folder
        self.scrap_button.setStyleSheet("border: none; color: white;")

        title_button_layout = QtWidgets.QHBoxLayout()
        title_button_layout.addWidget(self.title_label)
        title_button_layout.addWidget(self.scrap_button, alignment=QtCore.Qt.AlignRight)

        self.author_label = QtWidgets.QLabel()
        self.author_label.setStyleSheet("color: white; font-size: 12px;")
        
        self.keyward_label = QtWidgets.QLabel()
        self.keyward_label.setStyleSheet("color: white; font-size: 10px;")

        self.conf_label = QtWidgets.QLabel()
        self.ref_count_label = QtWidgets.QLabel()

        conf_ref_count_layout = QtWidgets.QHBoxLayout()
        conf_ref_count_layout.addWidget(self.conf_label)
        conf_ref_count_layout.addWidget(self.ref_count_label, alignment=QtCore.Qt.AlignRight)

        paper_layout = QtWidgets.QVBoxLayout(self)
        paper_layout.addLayout(title_button_layout)
        paper_layout.addWidget(self.author_label)
        paper_layout.addWidget(self.keyward_label)
        paper_layout.addLayout(conf_ref_count_layout)

    def update(self) :
        if self.paper is None :
            return
        
        if self.paper.title is not None :
            self.title_label.setText(self.paper.title)
        else :
            self.title_label.setText("NULL")
        
        if self.paper.author_list is not None :
            author_name_lsit = list(map(lambda author: author.name, self.paper.author_list))
            self.author_label.setText(", ".join(author_name_lsit))
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

        self.menu_function_map = {
            "Title" : self.query_handler.paperByTitle,
            #"DOI"   : lambda doi : self.query_handler.paperByDOI(doi, exact=True),
            "Author" : self.query_handler.paperByAuthor,
            "Keywords" : self.query_handler.paperByKeywards,
            "Conference" : self.query_handler.paperByConference,
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
            print(type(paper))
            item = PaperClipSearchResultItem(self, paper)
            #item = PaperItem(self, paper)
            item_list.append(item)
        self.scrollable.update(item_list)


    def itemClicked(self, paper) :
        self.parent.paperItemClicked(paper)