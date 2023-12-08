from pprint import pprint


from PyQt5 import QtWidgets, QtCore, QtGui


class PaperItem(QtWidgets.QWidget):
    def __init__(
            self,
            parent,
            paper,
            true_icon_str = "\U0001F4CE",
            false_icon_str = "\U0001F4C1"

        ):
        super().__init__(parent=parent)
        self.setStyleSheet("background-color: #303030; border-bottom: 1px solid white;")
        self.mousePressEvent = self.itemClicked
        
        self.parent = parent
        self.true_icon_str = true_icon_str
        self.false_icon_str = false_icon_str
        self.paper = paper
        title = paper.title
        if not title:
            if paper.DOI is not None:
                title = paper.DOI
            else :
                title = "Null"

        self.title_label = QtWidgets.QLabel(title)
        self.title_label.setStyleSheet("""
            QLabel {
                color: white;
                background-color: #303030;
                border-style: none;
            }
        """)
        self.title_label.setWordWrap(True)

        self.heartButton = QtWidgets.QPushButton(
            self.true_icon_str if paper.is_in_favorite else self.false_icon_str
        )
        self.heartButton.setFixedSize(QtCore.QSize(30, 30))
        self.heartButton.setStyleSheet("""
            QPushButton {
                background-color: #303030;
                border-style: none;
            }
        """) 
        self.heartButton.clicked.connect(self.favorite_list_changed)

        h_layout = QtWidgets.QHBoxLayout()
        h_layout.addWidget(self.title_label)
        h_layout.addWidget(self.heartButton)
        title_and_button_widget = QtWidgets.QWidget()
        title_and_button_widget.setLayout(h_layout)

        v_layout = QtWidgets.QVBoxLayout()
        v_layout.addWidget(title_and_button_widget)

        self.setLayout(v_layout)

    def itemClicked(self, event):
        self.parent.itemClicked(self.paper)

    def authorClicked(self, event):
        print("author clicked")

    def toggleHeart(self):
        self.heartButton.setText(
            self.true_icon_str if self.paper.is_in_favorite else self.false_icon_str)

    def favorite_list_changed(self):
        if self.paper.authors is None:
            return
        
        self.paper.toggleFavorite()
        self.toggleHeart()

        self.parent.favorite_list_changed(self.paper)