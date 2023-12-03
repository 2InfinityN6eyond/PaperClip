import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView

PDFJS_PATH = "./pdf.js/web/viewer.html"
FILE_PATH = "/Users/hjp/Downloads/lab10-gui3.pdf"

class PDFViewer(QMainWindow):
    def __init__(
        self,
        pdfjs_path=PDFJS_PATH,
        file_path=FILE_PATH,
    ):
        super().__init__()
        self.initUI(pdfjs_path, file_path)

    def initUI(self, pdfjs_path, file_path):
        self.browser = QWebEngineView()

        # Path to the PDF.js viewer and the PDF file - adjust these paths as necessary
        pdfjs_path = os.path.abspath(pdfjs_path)
        pdf_file = os.path.abspath(file_path)

        # Construct the URL to open the PDF file using PDF.js
        url = QUrl.fromUserInput(f'file://{pdfjs_path}?file={pdf_file}')

        self.browser.load(url)
        self.setCentralWidget(self.browser)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = PDFViewer()
    sys.exit(app.exec_())
