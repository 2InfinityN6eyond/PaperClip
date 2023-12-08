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

        self.paper_meta_viewer = PaperMetaViewer(self.paper)
        self.paper_meta_viewer.show()
        self.paper_meta_viewer.setStyleSheet("background-color: #303030;")

        # Related Work 레이블
        related_work_label = QtWidgets.QLabel("Related Work")
        related_work_label.setStyleSheet("color: white;font-size: 18px; border-bottom: 1px solid white; font-weight: bold;")
        #related_work_label.setStyleSheet("color: white; background-color: #303030;")

        self.related_works_scrollable = ScrollableList(self)

        v_layout = QtWidgets.QVBoxLayout(self)
        v_layout.addWidget(self.paper_meta_viewer)
        v_layout.addWidget(related_work_label)
        v_layout.addWidget(self.related_works_scrollable)
        # v_layout.setStyleSheet("color: white; background-color: #303030;")


    def update(self, paper):
        self.paper = paper
        self.paper_meta_viewer.update(self.paper)

        paper_item_list = []
        if self.paper is None or self.paper.reference_list is None:
            return
        
        for ref in self.paper.reference_paper_list:
            if ref.title.startswith('1') == False:
                paper_item = PaperItem(self.related_works_scrollable, ref)
                paper_item_list.append(paper_item)

        self.related_works_scrollable.update(paper_item_list)

    def itemClicked(self, item) :
        related_paper_gui = RelatedPaperGUI(self, item)
        related_paper_gui.exec_()

    def favorite_list_changed(self, item):
        self.parent.favorite_list_changed(item)

