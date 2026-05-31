import sys
from PyQt6.QtWidgets import QApplication, QPushButton

app = QApplication(sys.argv)

# Create a Qt widget, which will be our window.
window = QPushButton("Push Me")
window.show()

app.exec()