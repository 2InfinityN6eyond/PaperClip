import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt  # Import the Qt module

#from PyQt6.QtWidgets import *
#from PyQt6.QtCore import Qt  # Import the Qt module

class SearchApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("background-color: #303030;")

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        splitter = QSplitter(self)
        splitter.setStyleSheet("background-color: #303030;")

        scraps_section = QWidget(splitter)
        scraps_section_layout = QVBoxLayout()

        # Scrap Viewer
        scrap_viewer = ScrapViewer()
        scraps_section_layout.addWidget(scrap_viewer)

        scraps_section.setLayout(scraps_section_layout)

        paper_section = QWidget(splitter)
        paper_layout = QVBoxLayout()
        paper_label = QLabel('Paper Information', paper_section)
        paper_label.setStyleSheet("color: white; font-size: 16px; border-bottom: 1px solid white;")
        self.paper_info = QLabel('검색 결과가 여기에 표시됩니다.', paper_section)
        self.paper_info.setStyleSheet("color: white;")
        paper_layout.addWidget(paper_label)
        paper_layout.addWidget(self.paper_info)
        paper_section.setLayout(paper_layout)

        center_section = QWidget(splitter)
        center_layout = QVBoxLayout()

        self.search_input = QLineEdit(self)
        self.search_input.setStyleSheet("color: white; background-color: #303030;")

        self.search_button = QPushButton('검색', self)
        self.search_button.setStyleSheet("color: black; background-color: white;")

        search_layout = QHBoxLayout()
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_button)

        spacer_label = QLabel(self)
        spacer_label.setStyleSheet("background-color: #505050;")

        center_layout.addLayout(search_layout)
        center_layout.addWidget(spacer_label)
        center_section.setLayout(center_layout)

        splitter.addWidget(scraps_section)
        splitter.addWidget(center_section)
        splitter.addWidget(paper_section)

        splitter.setHandleWidth(1)
        splitter.setStyleSheet("QSplitter::handle{background: white;}")
        # splitter.setStyleSheet("QSplitter::handle{background: white;}")

        layout.addWidget(splitter)
        self.setLayout(layout)

        self.search_button.clicked.connect(self.search_button_clicked)

        self.setGeometry(100, 100, 800, 400)
        self.setWindowTitle('검색 어플리케이션')

    def search_button_clicked(self):
        search_term = self.search_input.text()
        self.paper_info.setText(f'"{search_term}"에 대한 검색 결과가 표시됩니다.')


class ScrapViewer(QFrame):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # 메인 레이아웃
        layout = QVBoxLayout()

        # 상단 Scrap 텍스트
        scrap_label = QLabel("Scraps")
        scrap_label.setStyleSheet("color: white; font-size: 16px; border-bottom: 1px solid white;")
        layout.addWidget(scrap_label)

        # 하단 Subframe
        subframe = QFrame(self)
        subframe.setFrameShape(QFrame.StyledPanel)
        subframe_layout = QVBoxLayout(subframe)

        # 제목과 Scrap 버튼
        for i in range(10):  # 예시로 3개의 자료 추가
            item_layout = QHBoxLayout()

            title_label = QLabel(f"제목 {i+1}")
            title_label.setStyleSheet("color: white;")
            scrap_button = QPushButton("♥")
            scrap_button.setStyleSheet("border: none; color: white;")
            
            # Connect the button click to a function that prints the title
            scrap_button.clicked.connect(lambda _, title=f"제목 {i+1}": print(title))

            # item_layout.addWidget(title_label)
            # item_layout.addWidget(scrap_button)
            item_layout.addWidget(title_label, alignment=Qt.AlignLeft)  # Align title to the left
            item_layout.addWidget(scrap_button, alignment=Qt.AlignRight)  # Align button to the right

            subframe_layout.addLayout(item_layout)

        # 나머지 공간을 채우기 위한 수직 정렬 추가
        subframe_layout.addStretch()
        self.setFixedWidth(200)
        # self.setFixedWidth(self.width() * 0.5)

        # ScrollArea 추가
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(subframe)

        layout.addWidget(scroll_area)

        self.setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SearchApp()
    window.show()
    sys.exit(app.exec_())