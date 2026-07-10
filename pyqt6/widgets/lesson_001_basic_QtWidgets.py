import sys
from time import sleep as sleep_for_n_seconds
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDateEdit,
    QDateTimeEdit,
    QDial,
    QDoubleSpinBox,
    QFontComboBox,
    QLabel,
    QLCDNumber,
    QLineEdit,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QSlider,
    QSpinBox,
    QTimeEdit,
    QVBoxLayout,
    QWidget,
)

src = "https://www.pythonguis.com/tutorials/pyqt6-widgets/"

doc_string = f"""Widgets App ({src=})
In Qt (and most User Interfaces), widget is the name given to a component of the UI that the user can interact with. User interfaces are made up of multiple widgets, arranged within the window.

This example shows a simple window with a variety of widgets.
The window contains a vertical layout with the following widgets:
{'_' * 80}
Widget         |  What it does
{'_' * 80}
QCheckBox      |  A checkbox
QComboBox      |  A dropdown list box
QDateEdit      |  For editing dates
QDateTimeEdit  |  For editing dates and datetimes
QDial          |  Rotatable dial
QDoubleSpinBox |  A number spinner for floats
QFontComboBox  |  A list of fonts
QLCDNumber     |  A quite ugly LCD display
QLabel         |  Just a label, not interactive
QLineEdit      |  Enter a line of text
QProgressBar   |  A progress bar
QPushButton    |  A button
QRadioButton   |  A toggle set, with only one active item
QSlider        |  A slider
QSpinBox       |  An integer spinner
QTimeEdit      |  For editing times

"""

print(f"{doc_string}{'_' * 80}")
#sleep_for_n_seconds(10)

# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Widgets App")

        layout = QVBoxLayout()
        widgets = [
            QCheckBox,
            QComboBox,
            QDateEdit,
            QDateTimeEdit,
            QDial,
            QDoubleSpinBox,
            QFontComboBox,
            QLCDNumber,
            QLabel,
            QLineEdit,
            QProgressBar,
            QPushButton,
            QRadioButton,
            QSlider,
            QSpinBox,
            QTimeEdit,
        ]

        for w in widgets:
            layout.addWidget(w())

        widget = QWidget()
        widget.setLayout(layout)

        # Set the central widget of the Window. Widget will expand
        # to take up all the space in the window by default.
        self.setCentralWidget(widget)

# app = QApplication(sys.argv)
# window = MainWindow()
# window.show()
# app.exec()