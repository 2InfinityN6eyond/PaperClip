import sys
from PyQt5 import QtWidgets
from argparse import ArgumentParser

# local import
from query_handler import QueryHandler
from main_window import MainWindow

BACKGROUND_COLOR = "#303030"

if __name__ == '__main__':
    args = ArgumentParser()
    args.add_argument('--host', type=str, default='localhost', help='database host')
    args.add_argument('--user', type=str, default='root', help='database user')
    args.add_argument('--passwd', type=str, default='1398', help='database password')
    args.add_argument('--db_use', type=str, default='relation_db_project', help='database name')
    args = args.parse_args()

    # initialize query handler, which is bridge between GUI and database
    query_handler = QueryHandler(
        host    = args.host,
        user    = args.user,
        passwd  = args.passwd,
        db_use  = args.db_use
    )
    # initialize PyQt5 application
    app = QtWidgets.QApplication(sys.argv)
    # initialize main window
    window = MainWindow(query_handler)
    window.show()
    # start PyQt5 event loop
    app.exec_()
    # exit
    sys.exit()