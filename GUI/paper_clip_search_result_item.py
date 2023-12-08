from PyQt5 import QtWidgets, QtCore, QtGui

from containers import Paper

# Result of PaperClip search
class PaperClipSearchResultItem(QtWidgets.QWidget) :
    '''
    Item class representing search result of each paper.
    '''
    
    def __init__(
        self,
        parent,
        paper: Paper,
        true_icon = "\U0001F4CE",
        false_icon = "\U0001F4C1"
    ) :
        super().__init__(parent=parent)
        self.mousePressEvent = self.itemClicked

        self.parent = parent
        self.paper = paper

        if (
            self.paper is not None
        ) and (
            self.paper.title is None
        ) and (
            self.paper.DOI is not None
        ) :
            self.paper.title = self.paper.DOI

        self.true_icon_str  = true_icon
        self.false_icon_str = false_icon

        self.initUI()
        self.update()

    def initUI(self) :
        # Set GUI of result Search in Centor section
        
        # Define title_label & scrap_button
        self.title_label = QtWidgets.QLabel()
        self.title_label.setStyleSheet(
            "color: white; font-size: 16px; border: none; margin: 0; padding: 0;")
        self.title_label.setWordWrap(True)

        self.scrap_button = QtWidgets.QPushButton(
            self.true_icon_str if self.paper.is_in_favorite else self.false_icon_str,
        ) #folder
        self.scrap_button.clicked.connect(self.favorite_list_changed)
        self.scrap_button.setStyleSheet(
            "border: none; color: white;")

        # Set title_button_layout as QHBoxLayout and Put title_label & scrap_button
        title_button_layout = QtWidgets.QHBoxLayout()
        title_button_layout.addWidget(self.title_label, stretch=8)
        title_button_layout.addStretch(1)
        title_button_layout.addWidget(self.scrap_button, alignment=QtCore.Qt.AlignRight)

        # Define author_label
        self.author_label = QtWidgets.QLabel()
        self.author_label.setStyleSheet(
            "color: white; font-size: 12px; border: none; margin: 0; padding: 0;")
        self.author_label.setWordWrap(True)

        # Define keyword_label
        self.keyword_label = QtWidgets.QLabel()
        self.keyword_label.setStyleSheet(
            "color: white; font-size: 10px; border: none; margin: 0; padding: 0;")
        self.keyword_label.setWordWrap(True)
        
        # Define conf_label
        self.conf_label = QtWidgets.QLabel()
        self.conf_label.setStyleSheet(
            "color: white; font-size: 10px; border: none; margin: 0; padding: 0;")
        self.conf_label.setFixedHeight(25)

        # Define ref_count_label
        self.ref_count_label = QtWidgets.QLabel()
        self.ref_count_label.setStyleSheet(
            "color: white; font-size: 10px; border: none; margin: 0; padding: 0;")
        
        # set conf_ref_count_layout and put conf_label, ref_count_label in it
        conf_ref_count_layout = QtWidgets.QHBoxLayout()
        conf_ref_count_layout.addWidget(self.conf_label)
        conf_ref_count_layout.addWidget(self.ref_count_label, alignment=QtCore.Qt.AlignRight)
        
        # Define paper_separator
        paper_separator = QtWidgets.QFrame()
        paper_separator.setFrameShape(QtWidgets.QFrame.HLine)
        paper_separator.setFrameShadow(QtWidgets.QFrame.Sunken)
        paper_separator.setLineWidth(2)

        # Define paper_layout and put all sub-frame Define above
        paper_layout = QtWidgets.QVBoxLayout(self)
        paper_layout.addLayout(title_button_layout)
        paper_layout.addWidget(self.author_label)
        paper_layout.addWidget(self.keyword_label)
        paper_layout.addLayout(conf_ref_count_layout)
        paper_layout.addWidget(paper_separator)

    def update(self) :
        # if something has None value, then set the text 'NULL'
        if self.paper is None : # if paper does not exist
            return

        if self.paper.title is not None : # if paper's title does not exist
            self.title_label.setText(self.paper.title)
        else :
            self.title_label.setText("NULL")
        
        if self.paper.authors is not None : # if paper's author does not exist
            author_text = ", ".join(self.paper.authors)


            self.author_label.setText(author_text)
        else :
            self.author_label.setText("NULL")
        
        if self.paper.keywords is not None : # if paper's keywords does not exist
            keyword_text = ", ".join(self.paper.keywords)
            self.keyword_label.setText(keyword_text)
            
            
        if self.paper.conference_acronym is not None : # if paper's conference_acronym does not exist
            self.conf_label.setText(self.paper.conference_acronym)
        else :
            self.conf_label.setText("NULL")

        if self.paper.referenced_num is not None : # if paper's referenced_num does not exist
            self.ref_count_label.setText(str(self.paper.referenced_num))
        else :
            self.ref_count_label.setText("NULL")
    
    # Update paper_section's item when item clicked
    def itemClicked(self, event) :
        print("item clicked")
        self.parent.itemClicked(self.paper)

    # change clip icon
    def toggleHeart(self) :
        self.scrap_button.setText(
            self.true_icon_str if self.paper.is_in_favorite else self.false_icon_str
        )

    # Change favorite list
    def favorite_list_changed(self) :
        if self.paper.authors is None :
            return    
        self.paper.toggleFavorite()
        self.toggleHeart()    

        self.parent.favorite_list_changed(self.paper)

