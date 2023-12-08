from PyQt5 import QtWidgets, QtGui, QtCore

# local import
from scrollable_list import ScrollableList
from paper_clip_search_result_item import PaperClipSearchResultItem

class PaperWithCountItem(QtWidgets.QWidget) :
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

        # define the keyword labels for each keywords with its index
        self.keyword_label = QtWidgets.QLabel(f"{self.idx+1}. {self.keyword}")
        self.keyword_label.setStyleSheet("color: white;font-size: 16px;")
        self.keyword_label.linkActivated.connect(lambda _, keyword=self.keyword: self.update_right_side(keyword))

        # define the number of papers in each keywords
        self.count_label = QtWidgets.QLabel(f"{self.count} papers")
        self.count_label.setStyleSheet("color: white;font-size: 12px;")

        # define a layout with boxes of keywords/paper count pairs
        self.layout = QtWidgets.QHBoxLayout()
        self.layout.addWidget(self.keyword_label, alignment=QtCore.Qt.AlignLeft)
        self.layout.addWidget(self.count_label, alignment=QtCore.Qt.AlignRight)

        self.setLayout(self.layout)

    def itemClicked(self, event): # when the item is clicked, propagate the information to parent
        self.parent.update_right_side(self.keyword)

class PopularPapersWindow(QtWidgets.QDialog):
    def __init__(
        self,
        parent,
        query_handler
    ):
        super().__init__(parent)
        self.query_handler = query_handler
        self.parent = parent

        # Set the background color
        self.setStyleSheet("background-color: #303030;")
        self.setGeometry(100, 100, 1200, 800)
        
        # popular keywords label with scrollable list defined
        popular_keywords_label = QtWidgets.QLabel('Popular Keywords')
        popular_keywords_label.setStyleSheet("color: white; font-size: 18px; border-bottom: 1px solid white; font-weight: bold;")
        
        self.paper_keyword_scrollable_list = ScrollableList(self)

        # display keywords in its popular order on a scrollable list
        left_layout = QtWidgets.QVBoxLayout()
        left_layout.addWidget(popular_keywords_label)
        left_layout.addWidget(self.paper_keyword_scrollable_list)

        left_widget = QtWidgets.QWidget()
        left_widget.setLayout(left_layout)


        # display the keyword that user clicked as a title, default as a placeholder
        self.placeholder_label = QtWidgets.QLabel('')
        self.placeholder_label.setStyleSheet("color: white; font-size: 18px; border-bottom: 1px solid white; font-weight: bold;")

        self.paper_scrollable_list = ScrollableList(self)

        # display a layout with the label of title label and scrollable list of papers
        right_layout = QtWidgets.QVBoxLayout()
        right_layout.addWidget(self.placeholder_label)
        right_layout.addWidget(self.paper_scrollable_list)

        right_widget = QtWidgets.QWidget()
        right_widget.setLayout(right_layout)

        # use splitter to automatically resize each sub-frames for viewing top keywords and papers
        splitter = QtWidgets.QSplitter(self)
        splitter.setStyleSheet("background-color: #303030;")
        splitter.setStyleSheet("QSplitter::handle{background: white;}")
        splitter.setHandleWidth(1)
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)

        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(splitter)
        self.setLayout(layout)

        self.updateKeywordList()

    def updateKeywordList(self):
        # change the keyword list
        keyword_count_list = self.query_handler.fetchTopKeywords()
        item_list = []
        for i, (keyword, count) in enumerate(keyword_count_list) :
            item = PaperWithCountItem(
                parent  = self,
                idx     = i,
                keyword = keyword,
                count   = count
            )
            item_list.append(item)
        self.paper_keyword_scrollable_list.update(item_list)
        
    def update_right_side(self, keyword):
        # update the placeholder label to the keyword that user selected
        self.placeholder_label.setText(f"{keyword}")
        paper_list = self.query_handler.queryPaperBy(
            by="p.keywords", value=keyword
        )
        # add the papers that are selected using the sql query
        item_list = []
        for i, paper in enumerate(paper_list) :
            item = PaperClipSearchResultItem(
                parent  = self,
                paper   = paper
            )
            item_list.append(item)
        self.paper_scrollable_list.update(item_list)

    def itemClicked(self, item): #testing
        print("item clicked")

    def favorite_list_changed(self, item): # when favorite list is changed, remove the item and propagate the information to parent
        self.parent.favorite_list_changed(item)