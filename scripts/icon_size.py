import sys
from PyQt5.QtWidgets import QApplication, QPushButton
import qtawesome as qta

app = QApplication(sys.argv)

# Create a larger icon by setting the font size
icon_options = {'font-size': '40pt'}  # Adjust the size as needed
large_icon = qta.icon('fa5s.heart', options=[icon_options])

# Create a QPushButton and set the large icon
button = QPushButton()
button.setIcon(large_icon)
button.setIconSize(large_icon.actualSize(button.size()))  # Adjust the button's icon size to fit the large icon

button.show()
sys.exit(app.exec_())
