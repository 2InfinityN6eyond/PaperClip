from PyQt5 import QtWidgets

# local import
from scrollable_list import ScrollableList
from popular_papers_window import PopularPapersWindow
from paper_clip_search_result_item import PaperClipSearchResultItem

# GUI corresponding to the middle section of the main page
class CenterSection(QtWidgets.QWidget) :
    def __init__(
        self,
        parent,
        query_handler
    ) :
        # give access to properties of a parent
        super().__init__()
        self.parent = parent
        self.query_handler = query_handler
        
        self.popular_papers_window = None

        # make buttons in GUI & Apply function
        most_popular_button = QtWidgets.QPushButton('View Popular Papers', self)
        most_popular_button.setStyleSheet("color: white; font-size: 18px; background-color: #505050;")
        most_popular_button.clicked.connect(self.view_most_popular_keywords)

        # Define dropdown menus and apply sql to each menu
        self.menu_function_map = {
            "Title" : lambda title : self.query_handler.queryPaperBy(
                by = "p.title", value = title
            ),
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
        self.dropdown_menu = QtWidgets.QComboBox(self)
        self.dropdown_menu.addItems(list(self.menu_function_map.keys()))
        self.dropdown_menu.setStyleSheet("color: white; background-color: #303030;")

        # Define search box and apply functions
        self.search_input = QtWidgets.QLineEdit(self)
        self.search_input.setStyleSheet("color: white; background-color: #303030;")
        self.search_input.returnPressed.connect(self.search_button_clicked)

        # Define search buttons and apply functions
        self.search_button = QtWidgets.QPushButton('Search', self)
        self.search_button.setStyleSheet("color: black; background-color: white;")
        self.search_button.clicked.connect(self.search_button_clicked)

        # Adding the features defined above to the QHBoxLayout
        search_layout = QtWidgets.QHBoxLayout()
        search_layout.addWidget(self.dropdown_menu)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_button)

        # Define ScrollableList
        self.scrollable = ScrollableList(self)

        # Adding the features defined above to the QVBoxLayout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(most_popular_button)
        layout.addLayout(search_layout)
        layout.addWidget(self.scrollable)
        self.setLayout(layout)
    
    # Define function when search button is clicked
    def search_button_clicked(self):
        # Get inputs from CenterSection
        serach_input = self.search_input.text()
        dropdown_menu = self.dropdown_menu.currentText()
        search_result = self.menu_function_map[dropdown_menu](serach_input)

        print(len(search_result), "results found")
        
        # Get papers from DB and save in item_list
        item_list = []
        for paper in search_result :
            item = PaperClipSearchResultItem(self, paper)
            item_list.append(item)

        # Update scrollable list items
        self.scrollable.update(item_list)

    # create view_most_popular_keywords Window
    def view_most_popular_keywords(self):
        self.popular_papers_window = PopularPapersWindow(
            self,
            query_handler=self.query_handler
        )
        self.popular_papers_window.exec_()

    # Update paper_section's item
    def itemClicked(self, paper) :
        self.parent.paperItemClicked(paper)

    # Change favorite list in clips
    def favorite_list_changed(self, item) :
        self.parent.favorite_list_changed(item)

    # Update all favorite lists that can be seen on the screen
    def favorite_list_changed_from_outside(self, item) :
        self.scrollable.favorite_list_changed_from_outside(item)