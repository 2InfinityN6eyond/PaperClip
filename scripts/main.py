from pprint import pprint

import os
import sys
import json
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QRect, Qt, pyqtSignal
from PyQt5.QtGui import QFont
from PyQt5.QtGui import *
#import mysql.connector

from containers import Paper, Author, Institution, Expertise, QueryHandler
from clickable_label import ClickableLabel
from scrap_viewer import ScrapViewer
from related_paper_gui import RelatedPaperGUI
from paper_gui import PaperGUI
from center_section import CenterSection
from popular_papers_window import PopularPapersWindow

import platform

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
        self.setGeometry(100, 100, 1200, 800)
        self.setWindowTitle('PaperClip')
        self.setStyleSheet("background-color: #303030;")

        self.query_handler = query_handler
        self.popular_papers_window = None

        splitter = QSplitter(self)
        splitter.setStyleSheet("background-color: #303030;")
        splitter.setStyleSheet("QSplitter::handle{background: white;}")
        splitter.setHandleWidth(1)
        
        self.scraps_section = ScrapViewer(parent=self)
        self.scraps_section.update(
            list(filter(
                lambda paper: paper.is_in_favorite,
                self.query_handler.whole_paper_dict.values())
            ))

        self.center_section = CenterSection(
            parent          = self,
            query_handler   = self.query_handler
        )
        
        self.paper_section = PaperGUI(
            parent = self,
            paper  = None
        )

        ##### 합치기
        splitter.addWidget(self.scraps_section)
        splitter.addWidget(self.center_section)
        splitter.addWidget(self.paper_section)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(splitter)
        self.setLayout(layout)


    def view_most_popular_keywords(self):
        print('clicked')
        popular_papers_window = PopularPapersWindow()
        popular_papers_window.exec_()

    def paperItemClicked(self, item) :
        self.paper_section.update(item)

    def favorite_list_changed(self, item):
        if item.authors is None :
            return
        if item.is_in_favorite:
            self.scraps_section.append(item)
            pass
        else :
            self.scraps_section.remove(item)
        self.paper_section.favorite_list_changed_from_outside(item)
        self.center_section.favorite_list_changed_from_outside(item)

if __name__ == '__main__':
    institution_dict = {}
    expertise_dict = {}
    whole_author_list = []
    whole_paper_dict = {}

    os_name = platform.system()

    INSTITUTION_FILE_PATH = "./data/institution_dict.json"
    if os.path.exists(INSTITUTION_FILE_PATH) :
        with open(INSTITUTION_FILE_PATH, "r", encoding='utf8') as f :
            institution_dict_raw = json.load(f)
        for k, v in institution_dict_raw.items() :
            institution_dict[k] = Institution(**v)

    EXPERTISE_FILE_PATH = "./data/expertise_dict.json"
    if os.path.exists(EXPERTISE_FILE_PATH) :
        with open(EXPERTISE_FILE_PATH, "r", encoding='utf8') as f :
            expertise_dict_raw = json.load(f)
        for k, v in expertise_dict_raw.items() :
            expertise_dict[k] = Expertise(**v)

    AUTHOR_FILE_PATH = "./data/author_list.json"
    if os.path.exists(AUTHOR_FILE_PATH) :
        with open(AUTHOR_FILE_PATH, "r", encoding='utf8') as f :
            author_list_raw = json.load(f)
        for author in author_list_raw :
            whole_author_list.append(Author(**author))

    WHOLE_PAPER_FILE_PATH = "./data/processed_paper_dict.json"
    WHOLE_PAPER_FILE_PATH = "./data/final_paper_dict.json"
    if os.path.exists(WHOLE_PAPER_FILE_PATH) :
        with open(WHOLE_PAPER_FILE_PATH, "r", encoding='utf8') as f :
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
    app.exec_()

    print("writing..")
    # save final_paper_dict
    whole_paper_dict_dict = {}
    for k, v in whole_paper_dict.items() :
        v.query_handler = None
        whole_paper_dict_dict[k] = v.toDict()
    with open(WHOLE_PAPER_FILE_PATH, "w", encoding='utf8') as f :
        json.dump(whole_paper_dict_dict, f, indent=4, ensure_ascii=False)

    sys.exit()