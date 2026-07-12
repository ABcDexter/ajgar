import sys
import time
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QComboBox, QMainWindow


doc_str = f"""
The QComboBox is a drop-down list, closed by default with an arrow to open it.
We can also set a flag to determine how the insert is handled.
{"_"*79}
PyQt6 flag (long name)                      | Behavior
{"_"*79}
QComboBox.InsertPolicy.NoInsert             | No insert
QComboBox.InsertPolicy.InsertAtTop          | Insert as first item
QComboBox.InsertPolicy.InsertAtCurrent      | Replace currently selected item
QComboBox.InsertPolicy.InsertAtBottom       | Insert after last item
QComboBox.InsertPolicy.InsertAfterCurrent   | Insert after current item
QComboBox.InsertPolicy.InsertBeforeCurrent  | Insert before current item
QComboBox.InsertPolicy.InsertAlphabetically | Insert in alphabetical order
{"_"*79}
"""

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        widget = QComboBox()
        widget.addItems(["One", "Two", "Three"])
        widget.setEditable(True)
        
        # Sends the current index (position) of the selected item.
        widget.currentIndexChanged.connect(self.index_changed)

        # There is an alternate signal to send the text.
        widget.currentTextChanged.connect(self.text_changed)

        self.setCentralWidget(widget)

    def index_changed(self, i:int):
        print(f"Index changed to {i}", end="... ")

    def text_changed(self, s:str):
        print(f"Text changed to {s}")

print(doc_str)
time.sleep(1)
app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()