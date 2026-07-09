import time
import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt6.QtGui import QFont

doc_str = """Event hierarchy (source = https://www.pythonguis.com/tutorials/pyqt6-signals-slots-events/#events)
In PyQt every widget is part of two distinct hierarchies: the Python object hierarchy, and the Qt layout hierarchy. 
How you respond or ignore events can affect how your UI behaves...

1. Python inheritance forwarding
    Often you may want to intercept an event, do something with it, yet still trigger the default event handling behavior. 
    If your object is inherited from a standard widget, it will likely have sensible behavior implemented by default. 
    You can trigger this by calling up to the parent implementation using super().

2. Layout forwarding
    When you add a widget to your application, it also gets another parent from the layout. 
    The parent of a widget can be found by calling .parent(). Sometimes you specify these parents manually, such as for QMenu or QDialog, often it is automatic. 
    When you add a widget to your main window for example, the main window will become the widget's parent.
    When events are created for user interaction with the UI, these events are passed to the uppermost widget in the UI. So, if you have a button on a window, and click the button, the button will receive the event first.
    If the first widget cannot handle the event, or chooses not to, the event will bubble up to the parent widget, which will be given a turn. This bubbling continues all the way up nested widgets, until the event is handled or it reaches the main window.
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

    def mouseReleaseEvent(self, event):
        print("Mouse released!")
        # Python inheritance forwarding
        #super().mouseReleaseEvent(event)
        event.accept()  # Accept the event to indicate it has been handled
        self.setWindowTitle("Mouse Released - Event Handled")

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
