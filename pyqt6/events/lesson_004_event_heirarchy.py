import time
import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt6.QtGui import QFont

doc_str = """Event hierarchy
In PyQt every widget is part of two distinct hierarchies: the Python object hierarchy, and the Qt layout hierarchy. 
How you respond or ignore events can affect how your UI behaves...
"""
print(f"Event Hierarchy : {doc_str}{'_' * 80}")
time.sleep(5)

# minimize the code below to focus on the event hierarchy and mouse events
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Mouse Press Checker")
        self.setGeometry(100, 100, 600, 400)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
            
    def mousePressEvent(self, event):
        print("Mouse pressed!")
        # Python inheritance forwarding
        super().mousePressEvent(event)
        self.setWindowTitle("Mouse Pressed - Event Handled")



app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
