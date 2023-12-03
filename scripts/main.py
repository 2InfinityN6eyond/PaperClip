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
from argparse import ArgumentParser
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
            self.query_handler.queryPaperBy(
                by="p.clip", value="1"
            )
        )

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

    args = ArgumentParser()
    args.add_argument('--host', type=str, default='localhost')
    args.add_argument('--user', type=str, default='root')
    args.add_argument('--passwd', type=str, default='1398')
    args.add_argument('--db_use', type=str, default='relation_db_project')
    args = args.parse_args()

    query_handler = QueryHandler(
        host    = args.host,
        user    = args.user,
        passwd  = args.passwd,
        db_use  = args.db_use
    )

    app = QApplication(sys.argv)
    window = SearchApp(query_handler)
    window.show()
    app.exec_()

    sys.exit()