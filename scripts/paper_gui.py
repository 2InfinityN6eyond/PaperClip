from PyQt5.QtWidgets import *

from scrollables import ScrollableList
from paper_meta_viewer import PaperMetaViewer
from related_paper_gui import RelatedPaperGUI
 

from paper_item import PaperItem

class PaperGUI(QWidget):
    def __init__(
        self,
        parent,
        paper
    ):
        super().__init__()
        self.parent = parent
        self.paper = paper
        self.init_ui()

    def init_ui(self):

        self.paper_meta_viewer = PaperMetaViewer(self.paper)

        # Related Work 레이블
        related_work_label = QLabel("Related Work")
        related_work_label.setStyleSheet("color: white;font-size: 18px; border-bottom: 1px solid white; font-weight: bold;")

        self.scrollable = ScrollableList(self)
        # self.scrollable = QScrollBar(self)
        # self.scrollable.setOrientation(Qt.Vertical)

        v_layout = QVBoxLayout(self)
        v_layout.addWidget(self.paper_meta_viewer)
        v_layout.addWidget(related_work_label)
        v_layout.addWidget(self.scrollable)

        self.update(self.paper)

    def update(self, paper):
        self.paper = paper
        self.paper_meta_viewer.update(self.paper)

        paper_item_list = []
        if paper is None or self.paper.reference_list is None:
            return
        
        for ref in self.paper.reference_paper_list:
            if ref.title.startswith('1') == False:
                paper_item = PaperItem(self.scrollable, ref)
                paper_item_list.append(paper_item)
                print(paper_item_list, paper_item)
        print(self.scrollable)
        self.scrollable.update(paper_item_list)


    def itemClicked(self, item) :
        print("item clicked")
        related_paper_gui = RelatedPaperGUI(self, item)
        related_paper_gui.exec_()


    def open_related_paper_gui(self, title, author):
        related_paper_info = self.get_related_paper_info(title, author)  # title을 통해 관련 논문 정보 가져오기

        # 새로운 GUI를 띄우기 위한 RelatedPaperGUI 인스턴스 생성
        related_paper_gui = RelatedPaperGUI(related_paper_info)
        related_paper_gui.exec_()
        
    def scrap_paper(self, title, author):
        print(f"Scrapped Paper - Title: {title}, Author: {author}")
        
    def print_title(self, title):
        print(f"Clicked Title: {title}")

    def print_author(self, author):
        print(f"Clicked Author: {author}")

    def favorite_list_changed(self, item):
        self.parent.favorite_list_changed(item)

    def favorite_list_changed_from_outside(self, item):
        self.scrollable.favorite_list_changed_from_outside(item)