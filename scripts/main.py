from pprint import pprint

import os
import sys
import json
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
#import mysql.connector

from containers import Paper, Author, Institution, Expertise, QueryHandler
from clickable_label import ClickableLabel
from scrap_viewer import ScrapViewer
from related_paper_gui import RelatedPaperGUI
from paper_gui import PaperGUI


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
    def __init__(
            self,
            query_handler
        ) :
        super().__init__()

        self.query_handler = query_handler

        self.popular_papers_window = None
        self.setStyleSheet("background-color: #303030;")

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        splitter = QSplitter(self)
        splitter.setStyleSheet("background-color: #303030;")

        scraps_section = QWidget(splitter)
        scraps_section_layout = QVBoxLayout()

        self.scrap_viewer = ScrapViewer(parent=self)
        self.scrap_viewer.update(
            list(self.query_handler.whole_paper_dict.values())[:200]
        )
        scraps_section_layout.addWidget(self.scrap_viewer)

        scraps_section.setLayout(scraps_section_layout)

        # Set size policy for scraps_section to be resizable
        scraps_section.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)


        self.paper_section = PaperGUI(paper)

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
        splitter.addWidget(self.paper_section)

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

    def paperItemClicked(self, item) :
        self.paper_section.update(item)


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


if __name__ == '__main__':
    institution_dict = {}
    expertise_dict = {}
    whole_author_list = []
    whole_paper_dict = {}

    INSTITUTION_FILE_PATH = "./data/institution_dict.json"
    if os.path.exists(INSTITUTION_FILE_PATH) :
        with open(INSTITUTION_FILE_PATH, "r") as f :
            institution_dict_raw = json.load(f)
        for k, v in institution_dict_raw.items() :
            institution_dict[k] = Institution(**v)

    EXPERTISE_FILE_PATH = "./data/expertise_dict.json"
    if os.path.exists(EXPERTISE_FILE_PATH) :
        with open(EXPERTISE_FILE_PATH, "r") as f :
            expertise_dict_raw = json.load(f)
        for k, v in expertise_dict_raw.items() :
            expertise_dict[k] = Expertise(**v)

    AUTHOR_FILE_PATH = "./data/author_list.json"
    if os.path.exists(AUTHOR_FILE_PATH) :
        with open(AUTHOR_FILE_PATH, "r") as f :
            author_list_raw = json.load(f)
        for author in author_list_raw :
            whole_author_list.append(Author(**author))

    WHOLE_PAPER_FILE_PATH = "./data/processed_paper_dict.json"
    if os.path.exists(WHOLE_PAPER_FILE_PATH) :
        with open(WHOLE_PAPER_FILE_PATH, "r") as f :
            whole_paper_dict = json.load(f)
        for k, v in whole_paper_dict.items() :
            whole_paper_dict[k] = Paper(**v)

    print(f"number of institution : {len(institution_dict)}")
    print(f"number of expertise : {len(expertise_dict)}")
    print(f"number of author : {len(whole_author_list)}")
    print(f"number of paper : {len(whole_paper_dict)}")

    query_handler = QueryHandler(
        whole_paper_dict = whole_paper_dict,
        whole_author_dict = whole_author_list,
        whole_institution_dict = institution_dict,
        whole_expertise_dict = expertise_dict,
    )
    for author in whole_author_list :
        author.query_handler = query_handler
    for paper in whole_paper_dict.values() :
        paper.query_handler = query_handler
    for institution in institution_dict.values() :
        institution.query_handler = query_handler
    for expertise in expertise_dict.values() :
        expertise.query_handler = query_handler


    app = QApplication(sys.argv)
    window = SearchApp(query_handler)
    window.show()
    sys.exit(app.exec_())