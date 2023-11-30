import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal

class ClickableLabel(QLabel):
    # 클릭 가능한 레이블 클래스 정의
    linkActivated = pyqtSignal(str)

    def __init__(self, text):
        super().__init__(text)
        self.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.setOpenExternalLinks(False)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.linkActivated.emit(self.text())

class PaperGUI(QWidget):
    def __init__(self, paper_info):
        super().__init__()

        self.paper_info = paper_info
        self.init_ui()

    def init_ui(self):
        # Paper Name 레이블
        paper_name_label = QLabel(self.paper_info['Paper Name'])
        paper_name_label.setStyleSheet("color: white; font-size: 20px; font-weight: bold;")

        # Author와 Keyword 레이블
        author_label = QLabel(f"Author: {self.paper_info['Author']}")
        author_label.setStyleSheet("color: white;")
        keyword_label = QLabel(f"Keywords: {self.paper_info['Keywords']}")
        keyword_label.setStyleSheet("color: white;")

        # Abstract 텍스트 에디터
        abstract_text = QTextEdit()
        abstract_text.setPlainText(self.paper_info['Abstract'])
        abstract_text.setReadOnly(True)
        abstract_text.setStyleSheet("color: white;")
        abstract_text.setFixedHeight(abstract_text.sizeHint().height())

        # Related Work 레이블
        related_work_label = QLabel("Related Work")
        related_work_label.setStyleSheet("color: white;font-size: 18px; font-weight: bold;")

        # Related Papers 프레임
        related_papers_frame = QFrame()
        related_papers_layout = QVBoxLayout(related_papers_frame)
        related_papers_layout.setAlignment(Qt.AlignTop)

        for related_paper in self.paper_info['Related Papers']:
            paper_layout = QHBoxLayout()

            paper_title_label = ClickableLabel(f"Title: {related_paper['Title']}")
            paper_title_label.setStyleSheet("color: white; font-size: 16px;")
            paper_author_label = ClickableLabel(f"Author: {related_paper['Author']}")
            paper_author_label.setStyleSheet("color: white; font-size: 16px;")
            scrap_button = QPushButton("♥")
            scrap_button.setStyleSheet("border: none; color: white;")

            paper_layout.addWidget(paper_title_label)
            paper_layout.addWidget(scrap_button, alignment=Qt.AlignRight)

            paper_separator = QFrame()
            paper_separator.setFrameShape(QFrame.HLine)
            paper_separator.setFrameShadow(QFrame.Sunken)
            paper_separator.setStyleSheet("background: gray;")

            scrap_button.clicked.connect(lambda _, title=related_paper['Title'], author=related_paper['Author']: self.scrap_paper(title, author))

            paper_title_label.linkActivated.connect(self.print_title)
            paper_author_label.linkActivated.connect(self.print_author)

            related_papers_layout.addLayout(paper_layout)
            related_papers_layout.addWidget(paper_author_label)
            related_papers_layout.addWidget(paper_separator)

        # Related Papers 스크롤 영역
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(related_papers_frame)

        # 전체 레이아웃 구성
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(paper_name_label)
        main_layout.addWidget(author_label)
        main_layout.addWidget(keyword_label)
        main_layout.addWidget(abstract_text)
        main_layout.addWidget(related_work_label)
        main_layout.addWidget(scroll_area)

        # self.setGeometry(100, 100, 800, 600)
        # self.setFixedSize(300, 600)
        self.setWindowTitle('Paper GUI')
        self.show()

    def scrap_paper(self, title, author):
        print(f"Scrapped Paper - Title: {title}, Author: {author}")
        
    def print_title(self, title):
        print(f"Clicked Title: {title}")

    def print_author(self, author):
        print(f"Clicked Author: {author}")

class SearchApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("background-color: #303030;")

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        splitter = QSplitter(self)
        splitter.setStyleSheet("background-color: #303030;")

        scraps_section = QWidget(splitter)
        scraps_section_layout = QVBoxLayout()

        # Scrap Viewer
        scrap_viewer = ScrapViewer()
        scraps_section_layout.addWidget(scrap_viewer)

        scraps_section.setLayout(scraps_section_layout)

        paper_section = PaperGUI({
            'Paper Name': 'Sample Paper',
            'Author': 'John Doe',
            'Keywords': 'Sample, Keywords',
            'Abstract': 'This is a sample abstract for the paper. ' * 10,
            'Related Papers': [
                {'Title': 'Related Paper 1', 'Author': 'Jane Doe'},
                {'Title': 'Related Paper 2', 'Author': 'Bob Smith'},
            ]
        })
        
        center_section = QWidget(splitter)
        center_layout = QVBoxLayout()

        self.search_input = QLineEdit(self)
        self.search_input.setStyleSheet("color: white; background-color: #303030;")

        self.search_button = QPushButton('검색', self)
        self.search_button.setStyleSheet("color: black; background-color: white;")

        search_layout = QHBoxLayout()
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_button)

        spacer_label = QLabel(self)
        spacer_label.setStyleSheet("background-color: #505050;")

        center_layout.addLayout(search_layout)
        center_layout.addWidget(spacer_label)
        center_section.setLayout(center_layout)

        splitter.addWidget(scraps_section)
        splitter.addWidget(center_section)
        splitter.addWidget(paper_section)

        splitter.setHandleWidth(1)
        splitter.setStyleSheet("QSplitter::handle{background: white;}")

        layout.addWidget(splitter)
        self.setLayout(layout)

        self.search_button.clicked.connect(self.search_button_clicked)

        self.setGeometry(100, 100, 800, 400)
        self.setWindowTitle('검색 어플리케이션')

    def search_button_clicked(self):
        search_term = self.search_input.text()
        # Assuming you want to update the paper information dynamically based on the search term
        # Update the paper_info dictionary accordingly
        updated_paper_info = {
            'Paper Name': f'Searched Paper - {search_term}',
            'Author': 'Searched Author',
            'Keywords': 'Searched Keywords',
            'Abstract': f'This is the abstract for the searched paper on "{search_term}". ' * 10,
            'Related Papers': [
                {'Title': 'Searched Related Paper 1', 'Author': 'Searched Author 1'},
                {'Title': 'Searched Related Paper 2', 'Author': 'Searched Author 2'},
            ]
        }
        self.paper_section.update_paper_info(updated_paper_info)

class ScrapViewer(QFrame):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # 메인 레이아웃
        layout = QVBoxLayout()

        # 상단 Scrap 텍스트
        scrap_label = QLabel("Scraps")
        scrap_label.setStyleSheet("color: white; font-size: 20px; font-weight: bold;")
        layout.addWidget(scrap_label)

        # 하단 Subframe
        subframe = QFrame(self)
        subframe.setFrameShape(QFrame.StyledPanel)
        subframe_layout = QVBoxLayout(subframe)

        # 제목과 Scrap 버튼
        for i in range(10):
            item_layout = QHBoxLayout()

            title_label = QLabel(f"제목 {i+1}")
            title_label.setStyleSheet("color: white;")
            scrap_button = QPushButton("♥")
            scrap_button.setStyleSheet("border: none; color: white;")
            
            # Connect the button click to a function that prints the title
            scrap_button.clicked.connect(lambda _, title=f"제목 {i+1}": print(title))

            item_layout.addWidget(title_label, alignment=Qt.AlignLeft)
            item_layout.addWidget(scrap_button, alignment=Qt.AlignRight)

            subframe_layout.addLayout(item_layout)

        subframe_layout.addStretch()
        self.setMinimumWidth(200)
        # self.setFixedWidth(250)
        # self.setFixedSize(300, 600)

        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(subframe)

        layout.addWidget(scroll_area)

        self.setLayout(layout)


class SearchApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("background-color: #303030;")

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        splitter = QSplitter(self)
        splitter.setStyleSheet("background-color: #303030;")

        scraps_section = QWidget(splitter)
        scraps_section_layout = QVBoxLayout()

        scrap_viewer = ScrapViewer()
        scraps_section_layout.addWidget(scrap_viewer)

        scraps_section.setLayout(scraps_section_layout)

        paper_section = PaperGUI({
            'Paper Name': 'Sample Paper',
            'Author': 'John Doe',
            'Keywords': 'Sample, Keywords',
            'Abstract': 'This is a sample abstract for the paper. ' * 10,
            'Related Papers': [
                {'Title': 'Related Paper 1', 'Author': 'Jane Doe'},
                {'Title': 'Related Paper 2', 'Author': 'Bob Smith'},
            ]
        })

        center_section = QWidget(splitter)
        center_layout = QVBoxLayout()

        self.search_input = QLineEdit(self)
        self.search_input.setStyleSheet("color: white; background-color: #303030;")

        self.search_button = QPushButton('검색', self)
        self.search_button.setStyleSheet("color: black; background-color: white;")

        search_layout = QHBoxLayout()
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_button)

        spacer_label = QLabel(self)
        spacer_label.setStyleSheet("background-color: #505050;")

        center_layout.addLayout(search_layout)
        center_layout.addWidget(spacer_label)
        center_section.setLayout(center_layout)

        splitter.addWidget(scraps_section)
        splitter.addWidget(center_section)
        splitter.addWidget(paper_section)

        splitter.setHandleWidth(1)
        splitter.setStyleSheet("QSplitter::handle{background: white;}")

        layout.addWidget(splitter)
        self.setLayout(layout)

        self.search_button.clicked.connect(self.search_button_clicked)

        self.setGeometry(100, 100, 1000, 500)
        self.setWindowTitle('검색 어플리케이션')

    def search_button_clicked(self):
        search_term = self.search_input.text()
        updated_paper_info = {
            'Paper Name': f'Searched Paper - {search_term}',
            'Author': 'Searched Author',
            'Keywords': 'Searched Keywords',
            'Abstract': f'This is the abstract for the searched paper on "{search_term}". ' * 10,
            'Related Papers': [
                {'Title': 'Searched Related Paper 1', 'Author': 'Searched Author 1'},
                {'Title': 'Searched Related Paper 2', 'Author': 'Searched Author 2'},
            ]
        }
        self.paper_section.update_paper_info(updated_paper_info)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SearchApp()
    window.show()
    sys.exit(app.exec_())

