import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QComboBox, QMainWindow


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        widget = QComboBox()
        widget.addItems(["One", "Two", "Three"])

        # Sends the current index (position) of the selected item.
        widget.currentIndexChanged.connect(self.index_changed)

        # There is an alternate signal to send the text.
        widget.currentTextChanged.connect(self.text_changed)

        self.setCentralWidget(widget)

    def index_changed(self, i:int):
        print(f"Index changed to {i}", end="... ")

    def text_changed(self, s:str):
        print(f"Text changed to {s}")


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()