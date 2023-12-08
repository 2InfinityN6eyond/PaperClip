from PyQt5 import QtCore, QtGui, QtWidgets 

from containers import Paper

class PaperMetaViewer(QtWidgets.QLabel):
    def __init__(self, paper: Paper):
        super().__init__()
        self.paper = paper
        self.initUI()

    def initUI(self):

        # paper Name label
        self.paper_name_label = QtWidgets.QTextBrowser()
        self.paper_name_label.setStyleSheet("color: white; font-size: 18px; border-bottom: 1px solid white; font-weight: bold;background-color: #303030;")

        # author and keyword label
        self.author_label = QtWidgets.QTextBrowser()
        self.author_label.setStyleSheet("color: white; font-size: 12px;background-color: #303030;")
        self.conf_label = QtWidgets.QLabel() #(f"Published from: {self.paper.conference}")
        self.conf_label.setStyleSheet("color: white; font-size: 12px;background-color: #303030;")

        # Abstract text editor for resiable text
        self.abstract_text = QtWidgets.QTextEdit()
        self.abstract_text.setPlainText("--------------") #(self.paper.abstract)
        self.abstract_text.setReadOnly(True)
        self.abstract_text.setStyleSheet("color: white;background-color: #303030;")
        self.abstract_text.setFixedHeight(self.abstract_text.sizeHint().height())

        # create main layout containing the widgets
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(self.paper_name_label)
        main_layout.addWidget(self.author_label)
        main_layout.addWidget(self.conf_label)
        main_layout.addWidget(self.abstract_text)

        self.update(self.paper)

    def update(self, paper):
        self.paper = paper
        if paper is None :
            return

        # for each title, author name, conference, abstract, update the label accordingly
        title = self.paper.title
        author_name_list = self.paper.authors
        conference = self.paper.conference_acronym
        abstract = self.paper.abstract_text

        self.paper_name_label.setText(title)
        self.author_label.setText(", ".join(author_name_list))
        self.conf_label.setText(f"Published from: {conference}")
        self.abstract_text.setPlainText(abstract)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.linkActivated.emit(self.text())
