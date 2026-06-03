#Events 
'''
Every interatction the user has with a Qt application is an event. 

When the user clicks a button, moves the mouse, or types on the keyboard, an event is generated. 
The application can respond to these events by defining event handlers, which are functions that are called when a specific event occurs.
'''

import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QTextEdit

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        label = QLabel("Click in this window")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label = label
        
        self.setCentralWidget(label)
    
    def mouseMoveEvent(self, event):
        self.label.setText("Mouse moved: %d, %d" % (event.position().x(), event.position().y()))
    
    def mousePressEvent(self, event):
        self.label.setText("Mouse pressed: %d, %d" % (event.position().x(), event.position().y()))
    
    def mouseReleaseEvent(self, event):
        self.label.setText("Mouse released: %d, %d" % (event.position().x(), event.position().y()))
    
    def mouseDoubleClickEvent(self, event):
        self.label.setText("Mouse double clicked: %d, %d" % (event.position().x(), event.position().y()))


app = QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()