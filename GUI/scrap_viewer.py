from PyQt5 import QtWidgets

from scrollable_list import ScrollableList
from paper_item import PaperItem

class ScrapViewer(QtWidgets.QFrame):
    def __init__(
        self,
        parent=None,
    ):
        super().__init__(parent=parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        # set the section and title of the bookmarked papers
        scrap_label = QtWidgets.QLabel("CLIPS")
        scrap_label.setStyleSheet("color: white; font-size: 18px; border-bottom: 1px solid white; font-weight: bold;")

        # create a scrollable list, then add all the widgets to the layout
        self.scrollable = ScrollableList(self)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(scrap_label)
        layout.addWidget(self.scrollable)
        self.setLayout(layout)
        
    
    def update(self, item_list) : # update all the papers in PaperItem to the layout when executed
        for item in item_list :
            paper_item = PaperItem(self, item)
            self.scrollable.scrollAreaLayout.addWidget(paper_item)

    def append(self, item) : # add PaperItem too the bookmarks
        paper_item = PaperItem(self, item)
        self.scrollable.scrollAreaLayout.addWidget(paper_item)

    def remove(self, item) : # remove PaperItem from the bookmarks area using DOI
        for i in reversed(range(self.scrollable.scrollAreaLayout.count())) :
            try :
                if self.scrollable.scrollAreaLayout.itemAt(i).widget().paper.DOI == item.DOI :
                    self.scrollable.scrollAreaLayout.itemAt(i).widget().setParent(None)
                    break
            except Exception as e :
                print(e)


    def itemClicked(self, item): # when the item is clicked, propagate the information to parent
        self.parent.paperItemClicked(item)

    def favorite_list_changed(self, item): # when favorite list is changed, remove the item and propagate the information to parent
        print("removing")
        self.remove(item)
        self.parent.favorite_list_changed(item)