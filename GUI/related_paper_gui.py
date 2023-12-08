from PyQt5 import QtWidgets 

# local import
from scrollable_list import ScrollableList
from paper_meta_viewer import PaperMetaViewer
from paper_item import PaperItem

class RelatedPaperGUI(QtWidgets.QDialog):
    def __init__(
        self,
        parent,
        paper
    ):
        super().__init__()
        self.setStyleSheet("background-color: #303030;")
        self.parent = parent
        self.paper = paper
        self.init_ui()
        self.update(self.paper)

    def init_ui(self):
        # define a viewer to see the meta data of the papers
        self.paper_meta_viewer = PaperMetaViewer(self.paper)
        self.paper_meta_viewer.show()
        self.paper_meta_viewer.setStyleSheet("background-color: #303030;")

        # Related Work label
        related_work_label = QtWidgets.QLabel("Related Work")
        related_work_label.setStyleSheet("color: white;font-size: 18px; border-bottom: 1px solid white; font-weight: bold;")

        # create a scrollable list for the related works and define the whole layout
        self.related_works_scrollable = ScrollableList(self)

        v_layout = QtWidgets.QVBoxLayout(self)
        v_layout.addWidget(self.paper_meta_viewer)
        v_layout.addWidget(related_work_label)
        v_layout.addWidget(self.related_works_scrollable)


    def update(self, paper):
        self.paper = paper
        self.paper_meta_viewer.update(self.paper)

        # bring the related works from the database
        paper_item_list = []
        if self.paper is None or self.paper.reference_list is None:
            return
        
        # if the referenced paper has data in the database (can be identified by startswith('1')),
        # add it to the list and display
        for ref in self.paper.reference_paper_list:
            if ref.title.startswith('1') == False:
                paper_item = PaperItem(self.related_works_scrollable, ref)
                paper_item_list.append(paper_item)

        self.related_works_scrollable.update(paper_item_list)

    def itemClicked(self, item) : # when the item is clicked, call RelatedPaperGUI and create new window
        related_paper_gui = RelatedPaperGUI(self, item)
        related_paper_gui.exec_()

    def favorite_list_changed(self, item): # when favorite list is changed, remove the item and propagate the information to parent
        self.parent.favorite_list_changed(item)

