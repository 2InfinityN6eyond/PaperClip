from PyQt5 import QtCore, QtWidgets

class ScrollableList(QtWidgets.QWidget):
    def __init__(
            self,
            parent=None,
            resizable=True,
            expand=True,
        ):
        super().__init__(parent=parent)

        # defining the area for scrolling the papers
        self.setStyleSheet("background-color: #303030;")

        self.parent = parent

        # use QVBoxLayout to define the widgets (paper information) inside the scroll box
        self.scrollArea = QtWidgets.QScrollArea()
        self.scrollArea.setWidgetResizable(resizable)

        # set paper information box to input in the layout
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.scrollAreaLayout.setAlignment(QtCore.Qt.AlignTop)

        # add it to the scroll layout
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.layout = QtWidgets.QVBoxLayout()
        self.scrollArea.verticalScrollBar().setValue(0)
        self.layout.insertLayout(0, self.scrollAreaLayout)
        self.layout.addWidget(self.scrollArea)
        self.setLayout(self.layout)

        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

    def update(self, item_list) :
        # empty the scrollarealayout
        for i in reversed(range(self.scrollAreaLayout.count())):
            if isinstance(self.scrollAreaLayout.itemAt(i), QtWidgets.QWidgetItem):
                self.scrollAreaLayout.itemAt(i).widget().setParent(None)

        # if there are no papers found from SQL query, display 'paper does not exist'
        if len(item_list) == 0:
            none_label = QtWidgets.QLabel()
            none_label.setText('Paper does not exist')
            none_label.setStyleSheet("color: white; font-size: 12px; border: none; margin: 0; padding: 0;")
            self.scrollAreaLayout.addWidget(none_label, alignment=QtCore.Qt.AlignCenter)
        
        # if there are papers, add it to the widget 
        for item in item_list :
            self.scrollAreaLayout.addWidget(item)

    def itemClicked(self, item):  # when the item is clicked, propagate the information to parent
        self.parent.itemClicked(item)

    def favorite_list_changed(self, item): # when favorite list is changed, propagate the information to parent
        self.parent.favorite_list_changed(item)

    def favorite_list_changed_from_outside(self, item): 
        # when favorite list is changed from other sections, change it on the widget as well
        for i in reversed(range(self.scrollAreaLayout.count())) :
            widget = self.scrollAreaLayout.itemAt(i).widget()
            if widget is not None :
                try :
                    if widget.paper.DOI == item.DOI :
                        widget.toggleHeart()
                        break
                except Exception as e :
                    print(e)
        

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    #mainWindow = MainWindow()
    mainWindow = ScrollableList()

    class ListItem(QtWidgets.QWidget):
        def __init__(
                self,
                text,
                is_in_favorite=False,
            ):
            super().__init__()
            self.setStyleSheet("background-color: #303030; border-bottom: 1px solid white;")

            self.is_in_favorite = is_in_favorite
            
            #layout for the paper scroll list
            self.layout = QtWidgets.QHBoxLayout()

            # text for paper
            self.label = QtWidgets.QLabel(text)
            self.label.setWordWrap(True)
            self.label.setStyleSheet("""
                QLabel {
                    background-color: #303030;
                    border-style: none;
                }
            """)

            # insert the clip icon for the bookmarked papers
            self.heartButton = QtWidgets.QPushButton()
            self.heartButton.setStyleSheet("""
                QPushButton {
                    background-color: #303030;
                    border-style: none;
                }
            """)
            self.heartButton.setFixedSize(QtCore.QSize(50, 50))

            self.heartButton.setIcon(self.false_icon)
            self.heartButton.setIconSize(self.false_icon.actualSize(self.heartButton.size()))
            self.heartButton.clicked.connect(self.toggleHeart)

            # set the layout for each paper's information
            self.layout.addWidget(self.label)
            self.layout.addWidget(self.heartButton)
            self.setLayout(self.layout)

        # Set icons for bookmarked papers
        def toggleHeart(self):
            self.is_in_favorite = not self.is_in_favorite
            if self.is_in_favorite:
                self.heartButton.setIcon(self.true_icon)
            else:
                self.heartButton.setIcon(self.false_icon)

    # test to check it working
    item_list = []
    for i in range(10):
        item_list.append(ListItem(f"제목 {i+1}"))
    mainWindow.update(item_list)
    mainWindow.show()
    sys.exit(app.exec_())
