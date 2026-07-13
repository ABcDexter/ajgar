# Imports
import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDial,
    QDoubleSpinBox,
    QLabel,
    QLineEdit,
    QListWidget,
    QMainWindow,
    QSlider,
    QSpinBox,
)


class MainWindow(QMainWindow):
    """
    MainWindow class that inherits from QMainWindow. 
    This class sets up the main window of the application and initializes various widgets.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My App")

        
        widget = QLabel("Hello")
        widget = QLabel("World")  # The label is created with the text : World
        widget.setText("Hello World!")   # The label now shows : Hello World

        font = widget.font()
        font.setPointSize(30)
        widget.setFont(font)
        widget.setAlignment(
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter
        )

        # widget.setPixmap(QPixmap("AbcDexter.jpeg"))  # Set the image to be displayed in the label
        # widget.setScaledContents(True)


        self.setCentralWidget(widget)


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()

