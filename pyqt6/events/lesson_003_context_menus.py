# Context Menus
import time

doc_str = """Signal based context menus are a more flexible way of handling context menus. 
Instead of overriding the .contextMenuEvent method, we can set a context menu policy on the widget and connect to the customContextMenuRequested signal.
This signal is emitted whenever a context menu is requested, and it passes the position of the mouse click as an argument.
Brilliant!!!
"""

print(f"Signal based : {doc_str}{'_' * 80}")
time.sleep(10)

import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication, QMainWindow, QMenu


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.show()

        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.on_context_menu)

    def on_context_menu(self, pos):
        context = QMenu(self)
        context.addAction(QAction("Action 1", self))
        context.addAction(QAction("Action 2", self))
        context.addAction(QAction("Action 3", self))
        context.exec(self.mapToGlobal(pos))


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()