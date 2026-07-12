import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QCheckBox, QMainWindow


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        widget = QCheckBox("This is a checkbox")
        widget.setCheckState(Qt.CheckState.Checked)

        #For tristate: 
        widget.setCheckState(Qt.CheckState.PartiallyChecked)
        # Or: widget.setTristate(True)
        widget.stateChanged.connect(self.show_state)

        self.setCentralWidget(widget)

    def show_state(self, s):
        print(f"State changed to {s}: ", end="")

        if s == Qt.CheckState.Checked.value:
            print("checked")
        elif s == Qt.CheckState.PartiallyChecked.value:
            print("partially checked")
        else:
            print("unchecked")

app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()