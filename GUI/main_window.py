from PyQt5 import QtWidgets

# local import 
from scrap_viewer import ScrapViewer
from paper_gui import PaperGUI
from center_section import CenterSection

class MainWindow(QtWidgets.QMainWindow):
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

        splitter = QtWidgets.QSplitter(self)
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


        splitter.addWidget(self.scraps_section)
        splitter.addWidget(self.center_section)
        splitter.addWidget(self.paper_section)

        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(splitter)
        self.central_window = QtWidgets.QWidget()
        self.central_window.setLayout(layout)
        self.setCentralWidget(self.central_window)


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
