import sys
from PyQt6.QtWidgets import QApplication, QLineEdit, QMainWindow
import time

doc_str = f"""

The QLineEdit has a number of signals available for different editing events including 
when return is pressed (by the user), when the user selection is changed. 
There are also two edit signals, one for when the text in the box has been edited 
and one for when it has been changed. The distinction here is between user edits and programmatic changes. 
The textEdited signal is only sent when the user edits text.
"""
class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        widget = QLineEdit()
        widget.setMaxLength(10)
        #widget.setText("Thou shalt NOT edit")
        widget.setPlaceholderText("Enter your name here")
        # so, it appears that setText() is not the same as setPlaceholderText()
        # because the setText sets the text of the QLineEdit, 
        # while the setPlaceholderText sets a placeholder text that is displayed when the QLineEdit is empty.
        # I wasn;t seeing the Selection changed signal being emitted when I was typing in the QLineEdit.
        #widget.setReadOnly(True) # uncomment this to make readonly

        widget.returnPressed.connect(self.return_pressed)
        widget.selectionChanged.connect(self.selection_changed)
        widget.textChanged.connect(self.text_changed)
        widget.textEdited.connect(self.text_edited)

        self.setCentralWidget(widget)

    def return_pressed(self):
        print("Return pressed!")
        self.centralWidget().setText("BOOM!")

    def selection_changed(self):
        print("Selection changed")
        print(self.centralWidget().selectedText())

    def text_changed(self, s):
        print("Text changed...")
        print(s)

    def text_edited(self, s):
        print("Text edited...")
        print(s)


print(doc_str)
time.sleep(1)
app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()