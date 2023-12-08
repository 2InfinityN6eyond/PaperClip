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
from main_window import MainWindow

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
    window = MainWindow(query_handler)
    window.show()
    app.exec_()

    sys.exit()