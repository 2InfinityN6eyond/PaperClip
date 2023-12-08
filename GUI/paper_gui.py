
from PyQt5 import QtWidgets

# local import
from containers import Paper
from scrollable_list import ScrollableList
from paper_meta_viewer import PaperMetaViewer
from related_paper_gui import RelatedPaperGUI
 

from paper_item import PaperItem

class PaperGUI(QtWidgets.QWidget):
    def __init__(
        self,
        parent,
        paper : Paper
    ):
        '''
        show following paper information :
            - title, author, conference, abstract, reference list
        args :
            parent : parent widget
            paper : Paper object
        '''
        super().__init__()
        self.setStyleSheet("background-color: #303030;")
        self.parent = parent
        self.paper = paper
        self.init_ui()
        self.update(self.paper)

    def init_ui(self):
        # Define PaperMetaViewer (reference PaperMetaViewer)
        self.paper_meta_viewer = PaperMetaViewer(self.paper)
        self.paper_meta_viewer.setStyleSheet("background-color: #303030;")
        # Related Work label
        related_work_label = QtWidgets.QLabel("Related Work")
        related_work_label.setStyleSheet("color: white;font-size: 18px; border-bottom: 1px solid white; font-weight: bold;")

        # Define scrollable
        self.scrollable = ScrollableList(self)
        
        # Define v_layout and add all sub-frames above
        v_layout = QtWidgets.QVBoxLayout(self)
        v_layout.addWidget(self.paper_meta_viewer)
        v_layout.addWidget(related_work_label)
        v_layout.addWidget(self.scrollable)

    def update(self, paper):
        # update paper_meta_viewer
        self.paper = paper
        self.paper_meta_viewer.update(self.paper)

        # Get reference paper lists
        paper_item_list = []
        if paper is None or self.paper.reference_list is None: # if there is no paper, or there is no reference paper
            return
        
        for ref in self.paper.reference_paper_list:
            if ref.title.startswith('1') == False:
                paper_item = PaperItem(self.scrollable, ref)
                paper_item_list.append(paper_item)
        self.scrollable.update(paper_item_list) # update scrollable so that we can see in GUI

    def itemClicked(self, item : Paper) :
        '''
        Callback function called when item inside self.scrollable is clicked.
        self.scrollable will take self as parent widget, and call this function when item is clicked.
        When called, this function will open new window to show information of clicked item.
        '''
        related_paper_gui = RelatedPaperGUI(self, item)
        related_paper_gui.exec_()
        
    def favorite_list_changed(self, item : Paper):
        '''
        Callback function called when 'clip' (scrap) button inside self.scrollable is clicked.
        self.scrollable will take self as parent widget, and call this function when clip button is clicked.
        When called, this function will propagate the event to parent widget,
        which will eventually propagate to every widget and then change 'clip' icon of corresponding item.
        '''
        self.parent.favorite_list_changed(item)

    def favorite_list_changed_from_outside(self, item : Paper):
        '''
        Callback function called when 'clip' (scrap) button from somewhere else is clicked.
        Parent of self will call this function when clip button is clicked.
        When clicked, this function will propagate the event to self.scrollable, 
        which will change 'clip' icon of corresponding item if item is in self.scrollable.
        '''
        self.scrollable.favorite_list_changed_from_outside(item)