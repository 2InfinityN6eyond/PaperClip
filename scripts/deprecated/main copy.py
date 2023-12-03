import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
#import mysql.connector

'''
def connect_to_database(db_use):
    mydb = mysql.connector.connect(
    host="localhost",
    user = "root",
    passwd = "wodud8115%",
    database = db_use
    )
    mycursor = mydb.cursor(prepared=True)
    return mydb, mycursor

# SQLite 데이터베이스 연결
mydb, cursor = connect_to_database("relation_db_project")
'''
"""cursor.execute("INSERT INTO author (name, affiliation, google_schorlar_profile_url) VALUES (?, ?, ?)",
                    (name, affiliation, google_schorlar_profile_url))"""

class SearchApp(QWidget):
    def __init__(self):
        super().__init__()
        self.popular_papers_window = None
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

        # Set size policy for scraps_section to be resizable
        scraps_section.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        paper_section = PaperGUI({
            'Paper Name': 'Sample Paper',
            'Author': 'John Doe',
            'Keywords': 'Sample, Keywords',
            'conf': 'IEEE',
            'Abstract': 'This is a sample abstract for the paper. ' * 10,
            'Related Papers': [
                {'Title': 'Related Paper 1', 'Author': 'Jane Doe', 'conf': 'IEEE'},
                {'Title': 'Related Paper 2', 'Author': 'Bob Smith', 'conf': 'IEEE'},
            ]
        })

        center_section = QWidget(splitter)
        center_layout = QVBoxLayout()

        # New button above the search section
        most_popular_button = QPushButton('View Popular Papers', self)
        most_popular_button.setStyleSheet("color: white; font-size: 18px; background-color: #505050;")
        most_popular_button.clicked.connect(self.view_most_popular_keywords)

        # Dropdown menu with five options
        self.dropdown_menu = QComboBox(self)
        self.dropdown_menu.addItems(["Title", "Author", "Keywords", "Conference"])
        self.dropdown_menu.setStyleSheet("color: white; background-color: #303030;")

        # Variable to store the selected item
        self.order_by = None

        # Connect the signal to the function to update the variable
        self.dropdown_menu.currentIndexChanged.connect(self.update_order_by)

        self.search_input = QLineEdit(self)
        self.search_input.setStyleSheet("color: white; background-color: #303030;")
        self.search_input.returnPressed.connect(self.search_button_clicked)

        self.search_button = QPushButton('Search', self)
        self.search_button.setStyleSheet("color: black; background-color: white;")

        search_layout = QHBoxLayout()
        search_layout.addWidget(self.dropdown_menu)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_button)


#####
        # Related Papers 프레임
        paper_info = {
        'Paper Name': 'Sample Paper',
        'Author': 'John Doe',
        'Keywords': 'Sample, Keywords',
        'conf': 'IEEE',
        'Abstract': 'This is a sample abstract for the paper. ' * 10,  # 텍스트 길이 조절을 위해 반복
        'Related Papers': [
            {'Title': 'Related Paper 1', 'Author': 'Jane Doe', 'ref': 100, 'keywords': 'NLP, ML', 'conf': 'IEEE', 'conf': 'IEEE',},
            {'Title': 'Related Paper 2', 'Author': 'Bob Smith', 'ref': 10, 'keywords': 'NLP, ML', 'conf': 'IEEE', 'conf': 'IEEE',},
        ]
        }
        
        related_papers_frame = QFrame()
        related_papers_layout = QVBoxLayout(related_papers_frame)
        related_papers_layout.setAlignment(Qt.AlignTop)  # 수직 정렬 추가

        for related_paper in paper_info['Related Papers']:
            paper_layout = QHBoxLayout()  # related paper 제목과 scrap 버튼을 수평으로 정렬하기 위한 레이아웃
            paper_title_label = ClickableLabel(f"{related_paper['Title']}")
            paper_title_label.setStyleSheet("color: white; font-size: 16px;")

            paper_author_label = ClickableLabel(f"Author: {related_paper['Author']}")
            paper_author_label.setStyleSheet("color: white; font-size: 12px;")

            paper_ref_label = ClickableLabel(f"Referenced: {related_paper['ref']}")
            paper_ref_label.setStyleSheet("color: white; font-size: 12px;")

            paper_keywords_label = ClickableLabel(f"Keywords: {related_paper['keywords']}")
            paper_keywords_label.setStyleSheet("color: white; font-size: 10px;")

            paper_conf_label = ClickableLabel(f"Published from: {related_paper['conf']}")
            paper_conf_label.setStyleSheet("color: white; font-size: 10px;")

            scrap_button = QPushButton("\U0001F4C1") #folder
            scrap_button.setStyleSheet("border: none; color: white;")

            paper_layout.addWidget(paper_title_label)
            paper_layout.addWidget(paper_ref_label)
            paper_layout.addWidget(scrap_button, alignment=Qt.AlignRight)

            paper_separator = QFrame()
            paper_separator.setFrameShape(QFrame.HLine)
            paper_separator.setFrameShadow(QFrame.Sunken)

            # Connect scrap button click event
            scrap_button.clicked.connect(lambda _, title=related_paper['Title'], author=related_paper['Author']: self.scrap_paper(title, author))

            paper_title_label.linkActivated.connect(self.print_title)
            paper_author_label.linkActivated.connect(self.print_author)

            related_papers_layout.addLayout(paper_layout)
            related_papers_layout.addWidget(paper_author_label)
            related_papers_layout.addWidget(paper_keywords_label)
            related_papers_layout.addWidget(paper_conf_label)
            related_papers_layout.addWidget(paper_separator)

        # Related Papers 스크롤 영역
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(related_papers_frame)

        center_layout.addWidget(most_popular_button)
        center_layout.addLayout(search_layout)
        center_layout.addWidget(scroll_area)
        center_section.setLayout(center_layout)


        ##### 합치기
        splitter.addWidget(scraps_section)
        splitter.addWidget(center_section)
        splitter.addWidget(paper_section)

        splitter.setHandleWidth(1)
        splitter.setStyleSheet("QSplitter::handle{background: white;}")

        layout.addWidget(splitter)
        self.setLayout(layout)

        self.search_button.clicked.connect(self.search_button_clicked)

        self.setGeometry(100, 100, 1200, 800)
        self.setWindowTitle('PaperClip')

    def search_button_clicked(self):
        search_term = self.search_input.text()
        dropdown_menu = self.dropdown_menu.currentText()
        print(search_term, dropdown_menu)
        """cursor.execute("INSERT INTO author (name, affiliation, google_schorlar_profile_url) VALUES (?, ?, ?)",
                    (name, affiliation, google_schorlar_profile_url))"""
        """if dropdown_menu == "Title":
            cursor.execute("")"""
        
        # self.paper_info.setText(f'"{search_term}"에 대한 검색 결과가 표시됩니다.')

    def update_order_by(self, index):
        # Update the order_by variable when the selection changes
        self.order_by = self.sender().currentText()
        print(self.order_by)

    def view_most_popular_keywords(self):
        print('clicked')
        popular_papers_window = PopularPapersWindow()
        popular_papers_window.exec_()

    def scrap_paper(self, title, author):
        print(f"Scrapped Paper - Title: {title}, Author: {author}")
        
    def print_title(self, title):
        print(f"Clicked Title: {title}")

    def print_author(self, author):
        print(f"Clicked Author: {author}")


class PaperGUI(QWidget):
    def __init__(self, paper_info):
        super().__init__()

        self.paper_info = paper_info
        self.init_ui()

    def init_ui(self):
        # Paper Name 레이블
        paper_name_label = QLabel(self.paper_info['Paper Name'])
        paper_name_label.setStyleSheet("color: white; font-size: 18px; border-bottom: 1px solid white; font-weight: bold;")

        # Author와 Keyword 레이블
        author_label = QLabel(f"Author: {self.paper_info['Author']}")
        author_label.setStyleSheet("color: white; font-size: 12px;")
        keyword_label = QLabel(f"Keywords: {self.paper_info['Keywords']}")
        keyword_label.setStyleSheet("color: white; font-size: 12px;")
        conf_label = QLabel(f"Published from: {self.paper_info['conf']}")
        conf_label.setStyleSheet("color: white; font-size: 12px;")


        # Abstract 텍스트 에디터
        abstract_text = QTextEdit()
        abstract_text.setPlainText(self.paper_info['Abstract'])
        abstract_text.setReadOnly(True)
        abstract_text.setStyleSheet("color: white;")
        abstract_text.setFixedHeight(abstract_text.sizeHint().height())

        # Related Work 레이블
        related_work_label = QLabel("Related Work")
        related_work_label.setStyleSheet("color: white;font-size: 18px; border-bottom: 1px solid white; font-weight: bold;")

        # Related Papers 프레임
        related_papers_frame = QFrame()
        related_papers_layout = QVBoxLayout(related_papers_frame)
        related_papers_layout.setAlignment(Qt.AlignTop)

        for related_paper in self.paper_info['Related Papers']:
            paper_layout = QHBoxLayout()

            paper_title_label = ClickableLabel(f"{related_paper['Title']}")
            paper_title_label.setStyleSheet("color: white; font-size: 16px;")
            paper_author_label = ClickableLabel(f"Author: {related_paper['Author']}")
            paper_author_label.setStyleSheet("color: white; font-size: 12px;")
            scrap_button = QPushButton("♥")
            scrap_button.setStyleSheet("border: none; color: white;")


            paper_layout.addWidget(paper_title_label)
            paper_layout.addWidget(scrap_button, alignment=Qt.AlignRight)

            paper_separator = QFrame()
            paper_separator.setFrameShape(QFrame.HLine)
            paper_separator.setFrameShadow(QFrame.Sunken)
            paper_separator.setStyleSheet("background: gray;")

            scrap_button.clicked.connect(lambda _, title=related_paper['Title'], author=related_paper['Author']: self.scrap_paper(title, author))

            paper_title_label.linkActivated.connect(lambda _, title=related_paper['Title'], author=related_paper['Author']: self.open_related_paper_gui(title, author))
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
        main_layout.addWidget(conf_label)
        main_layout.addWidget(abstract_text)
        main_layout.addWidget(related_work_label)
        main_layout.addWidget(scroll_area)


        self.setWindowTitle('Paper GUI')
        self.show()
        
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

class RelatedPaperGUI(QDialog):
    def __init__(self, paper_info):
        super().__init__()

        self.paper_info = paper_info
        self.init_ui()

    def init_ui(self):
        # Paper Name 레이블
        paper_name_label = QLabel(self.paper_info['Paper Name'])
        paper_name_label.setStyleSheet("color: white; font-size: 18px; border-bottom: 1px solid white; font-weight: bold;")

        # Author와 Keyword 레이블
        author_label = QLabel(f"Author: {self.paper_info['Author']}")
        author_label.setStyleSheet("color: white; font-size: 12px;")
        keyword_label = QLabel(f"Keywords: {self.paper_info['Keywords']}")
        keyword_label.setStyleSheet("color: white; font-size: 12px;")
        conf_label = QLabel(f"Published from: {self.paper_info['conf']}")
        conf_label.setStyleSheet("color: white; font-size: 12px;")

        # Abstract 텍스트 에디터
        abstract_text = QTextEdit()
        abstract_text.setPlainText(self.paper_info['Abstract'])
        abstract_text.setReadOnly(True)
        abstract_text.setStyleSheet("color: white;")
        abstract_text.setFixedHeight(abstract_text.sizeHint().height())

        # Related Work 레이블
        related_work_label = QLabel("Related Work")
        related_work_label.setStyleSheet("color: white;font-size: 18px; border-bottom: 1px solid white; font-weight: bold;")

        # Related Papers 프레임
        related_papers_frame = QFrame()
        related_papers_layout = QVBoxLayout(related_papers_frame)
        related_papers_layout.setAlignment(Qt.AlignTop)

        for related_paper in self.paper_info['Related Papers']:
            paper_layout = QHBoxLayout()

            paper_title_label = ClickableLabel(f"{related_paper['Title']}")
            paper_title_label.setStyleSheet("color: white; font-size: 16px;")
            paper_author_label = ClickableLabel(f"Author: {related_paper['Author']}")
            paper_author_label.setStyleSheet("color: white; font-size: 12px;")
            scrap_button = QPushButton("♥")
            scrap_button.setStyleSheet("border: none; color: white;")


            paper_layout.addWidget(paper_title_label)
            paper_layout.addWidget(scrap_button, alignment=Qt.AlignRight)

            paper_separator = QFrame()
            paper_separator.setFrameShape(QFrame.HLine)
            paper_separator.setFrameShadow(QFrame.Sunken)
            paper_separator.setStyleSheet("background: gray;")

            scrap_button.clicked.connect(lambda _, title=related_paper['Title'], author=related_paper['Author']: self.scrap_paper(title, author))

            paper_title_label.linkActivated.connect(self.open_related_paper_gui)
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
        main_layout.addWidget(conf_label)
        main_layout.addWidget(abstract_text)
        main_layout.addWidget(related_work_label)
        main_layout.addWidget(scroll_area)

        self.setWindowTitle(self.paper_info['Paper Name'])
        self.setStyleSheet("background-color: #303030;")
        self.setGeometry(200, 200, 800, 600)
        
    def open_related_paper_gui(self, title):
        related_paper_info = self.get_related_paper_info(title)  # title을 통해 관련 논문 정보 가져오기

        # 새로운 GUI를 띄우기 위한 RelatedPaperGUI 인스턴스 생성
        related_paper_gui = RelatedPaperGUI(related_paper_info)
        related_paper_gui.exec_()
    
    def get_related_paper_info(self, title):
        # title을 이용하여 관련 논문의 정보를 가져오는 함수 (실제로는 데이터베이스 조회 등이 필요)
        # 여기서는 간단한 예시로 더미 데이터를 반환
        return {
            'GUI' : '1010101',
            'Paper Name': f'{title}',
            'Author': 'Unknown Author',
            'conf': 'IEEE',
            'Keywords': 'Related, Keywords',
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

class PopularPapersWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Set the background color
        self.setStyleSheet("background-color: #303030;")
        self.setGeometry(100, 100, 1200, 800)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        splitter = QSplitter(self)
        splitter.setStyleSheet("background-color: #303030;")

        # Left section with popular keywords
        left_widget = QWidget(splitter)
        left_layout = QVBoxLayout()

        popular_keywords_label = QLabel('Popular Keywords')
        popular_keywords_label.setStyleSheet("color: white; font-size: 18px; border-bottom: 1px solid white; font-weight: bold;")
        left_layout.addWidget(popular_keywords_label)

        subframe = QFrame(self)
        subframe.setFrameShape(QFrame.StyledPanel)
        subframe_layout = QVBoxLayout(subframe)

        keywords_list = [
            ('NLP', '130'),
            ('Computer Vision', '120'),
            ('NLP', '110'),
            ('ㅜㅜ', '190'),
            ('NLP', '130'),
            ('하...', '130'),
            ('NLP', '130'),
            ('살려줘', '130'),
            ('NLP', '130'),
            ('NLP', '130'),
            ('NLP', '130'),
        ]

        for i, keywords in enumerate(keywords_list):
            keyword_label = ClickableLabel(f"{i + 1}. {keywords[0]}")
            keyword_label.setStyleSheet("color: white;font-size: 16px;")
            keyword_label.linkActivated.connect(lambda _, keyword=keywords[0]: self.update_right_side(keyword))


            ref_label = QLabel(f"{keywords[1]} papers")
            ref_label.setStyleSheet("color: white;font-size: 12px;")

            item_layout = QHBoxLayout()
            item_layout.addWidget(keyword_label, alignment=Qt.AlignLeft)
            item_layout.addWidget(ref_label, alignment=Qt.AlignRight)

            subframe_layout.addLayout(item_layout)

        subframe_layout.addStretch()
        subframe.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(subframe)
        left_layout.addWidget(scroll_area)

        left_widget.setLayout(left_layout)


        # Right section with NLP title, order by label, and dropdown
        right_widget = QWidget(splitter)
        right_layout = QVBoxLayout()

        label_and_dropdown_layout = QHBoxLayout()

        self.popular_label = QLabel('')
        self.popular_label.setStyleSheet("color: white; font-size: 18px; border-bottom: 1px solid white; font-weight: bold;")
        label_and_dropdown_layout.addWidget(self.popular_label)

        # Add a QComboBox for dropdown
        self.order_by_dropdown = QComboBox(self)
        self.order_by_dropdown.addItems(["Title", "Author", "Keywords", "Reference", "Conference"])  # Add your options here
        self.order_by_dropdown.setStyleSheet("color: white; background-color: #303030;")
        self.order_by_dropdown.setFixedWidth(100)  # Set the desired width
        label_and_dropdown_layout.addWidget(self.order_by_dropdown)

        # Add the QHBoxLayout to the main QVBoxLayout
        right_layout.addLayout(label_and_dropdown_layout)

        self.order_by_dropdown.currentIndexChanged.connect(self.update_selected_option)

        # Related Papers 프레임
        paper_info = {
        'Paper Name': 'Sample Paper',
        'Author': 'John Doe',
        'Keywords': 'Sample, Keywords',
        'conf': 'IEEE',
        'Abstract': 'This is a sample abstract for the paper. ' * 10,  # 텍스트 길이 조절을 위해 반복
        'Related Papers': [
            {'Title': 'Related Paper 1', 'Author': 'Jane Doe', 'ref': 100, 'keywords': 'NLP, ML', 'conf': 'IEEE'},
            {'Title': 'Related Paper 2', 'Author': 'Bob Smith', 'ref': 10, 'keywords': 'NLP, ML', 'conf': 'IEEE'},
        ]
        }

        related_papers_frame = QFrame()
        subframe.setFrameShape(QFrame.StyledPanel)
        related_papers_layout = QVBoxLayout(related_papers_frame)
        related_papers_layout.setAlignment(Qt.AlignTop)  # 수직 정렬 추가

        for related_paper in paper_info['Related Papers']:
            paper_layout = QHBoxLayout()  # related paper 제목과 scrap 버튼을 수평으로 정렬하기 위한 레이아웃
            paper_title_label = ClickableLabel(f"{related_paper['Title']}")
            paper_title_label.setStyleSheet("color: white; font-size: 16px;")

            paper_author_label = ClickableLabel(f"Author: {related_paper['Author']}")
            paper_author_label.setStyleSheet("color: white; font-size: 12px;")

            paper_ref_label = ClickableLabel(f"Referenced: {related_paper['ref']}")
            paper_ref_label.setStyleSheet("color: white; font-size: 12px;")

            paper_keywords_label = ClickableLabel(f"Keywords: {related_paper['keywords']}")
            paper_keywords_label.setStyleSheet("color: white; font-size: 10px;")

            paper_conf_label = ClickableLabel(f"Published from: {related_paper['conf']}")
            paper_conf_label.setStyleSheet("color: white; font-size: 10px;")

            scrap_button = QPushButton("♥")
            scrap_button.setStyleSheet("border: none; color: white;")

            paper_layout.addWidget(paper_title_label)
            paper_layout.addWidget(paper_ref_label)
            paper_layout.addWidget(scrap_button, alignment=Qt.AlignRight)

            paper_separator = QFrame()
            paper_separator.setFrameShape(QFrame.HLine)
            paper_separator.setFrameShadow(QFrame.Sunken)

            # Connect scrap button click event
            scrap_button.clicked.connect(lambda _, title=related_paper['Title'], author=related_paper['Author']: self.scrap_paper(title, author))

            paper_title_label.linkActivated.connect(self.print_title)
            paper_author_label.linkActivated.connect(self.print_author)

            related_papers_layout.addLayout(paper_layout)
            related_papers_layout.addWidget(paper_author_label)
            related_papers_layout.addWidget(paper_keywords_label)
            related_papers_layout.addWidget(paper_conf_label)
            related_papers_layout.addWidget(paper_separator)

        # Related Papers 스크롤 영역
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(related_papers_frame)

        right_layout.addWidget(scroll_area)
        right_widget.setLayout(right_layout)

        # 합치기
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)

        splitter.setHandleWidth(1)
        splitter.setStyleSheet("QSplitter::handle{background: white;}")

        layout.addWidget(splitter)
        self.setLayout(layout)

    def update_right_side(self, keyword):
        print(f"Clicked Keyword: {keyword}")
        self.popular_label.setText(keyword)

    def scrap_paper(self, title, author):
        print(f"Scrapped Paper - Title: {title}, Author: {author}")
        
    def print_title(self, title):
        print(f"Clicked Title: {title}")

    def print_author(self, author):
        print(f"Clicked Author: {author}")

    def update_selected_option(self, index):
        selected_option = self.order_by_dropdown.currentText()
        print(f"Selected Option: {selected_option}")

class ScrapViewer(QFrame):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        scrap_label = QLabel("CLIPS")
        scrap_label.setStyleSheet("color: white; font-size: 18px; border-bottom: 1px solid white; font-weight: bold;")
        layout.addWidget(scrap_label)

        subframe = QFrame(self)
        subframe.setFrameShape(QFrame.StyledPanel)
        subframe_layout = QVBoxLayout(subframe)

        for i in range(10):
            title_label = QLabel(f"제목 {i+1}")
            title_label.setStyleSheet("color: white;")

            scrap_button = QPushButton("\U0001F4CE") #clip
            scrap_button.setStyleSheet("border: none; color: white;")

            scrap_button.clicked.connect(lambda _, title=f"제목 {i+1}": print(title))

            item_layout = QHBoxLayout()
            item_layout.addWidget(title_label, alignment=Qt.AlignLeft)
            item_layout.addWidget(scrap_button, alignment=Qt.AlignRight)

            subframe_layout.addLayout(item_layout)

        subframe_layout.addStretch()
        subframe.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(subframe)

        layout.addWidget(scroll_area)

        self.setLayout(layout)



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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SearchApp()
    window.show()
    sys.exit(app.exec_())