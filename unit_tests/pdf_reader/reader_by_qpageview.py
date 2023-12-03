
import qpageview
import sys
import os
from PyQt5 import QtWidgets, QtGui, QtCore

FILE_PATH = "~/Downloads/4434_edge_aware_3d_instance_segment.pdf"
FILE_PATH = "~/Downloads/231011 (1).pdf"
FILE_PATH = "/Users/hjp/Downloads/lab10-gui3.pdf"
a = QtWidgets.QApplication(sys.argv)

v = qpageview.View()
v.show()
v.loadPdf(FILE_PATH)

print(os.path.exists(FILE_PATH))

a.exec_()