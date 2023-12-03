from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

from clickable_label import ClickableLabel
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
    
    def get_related_paper_info(self, title, author):
        # title을 이용하여 관련 논문의 정보를 가져오는 함수 (실제로는 데이터베이스 조회 등이 필요)
        # 여기서는 간단한 예시로 더미 데이터를 반환
        return {
            'Paper Name': f'{title}',
            'Author': f'{author}',
            'Keywords': 'Related, Keywords',
            'conf': 'IEEE',
            'Abstract': 'This is the abstract for the related paper.',
            'Related Papers': [{'Title': 'Related Paper 1', 'Author': 'Jane Doe', 'ref': 100, 'keywords': 'NLP, ML', 'conf': 'IEEE',},
            {'Title': 'Related Paper 2', 'Author': 'Bob Smith', 'ref': 10, 'keywords': 'NLP, ML', 'conf': 'IEEE',},]
        
        }
        
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