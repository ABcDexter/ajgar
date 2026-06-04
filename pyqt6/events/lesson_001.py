#Events - Mouse Cursor Tracking
'''
A comprehensive UI for live mouse cursor tracking in PyQt6.

Displays:
- Current mouse position (global and relative)
- Mouse button states
- Real-time cursor tracking
- Event statistics
'''

import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt6.QtGui import QFont

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Mouse Cursor Tracker")
        self.setGeometry(100, 100, 600, 400)
        
        # Initialize statistics
        self.move_count = 0
        self.click_count = 0
        self.release_count = 0
        self.double_click_count = 0
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Create labels for different information
        self.position_label = QLabel("Position: (0, 0)")
        self.relative_label = QLabel("Relative: (0, 0)")
        self.button_label = QLabel("Button: None")
        self.event_label = QLabel("Event: Waiting...")
        self.stats_label = QLabel("Stats - Moves: 0 | Clicks: 0 | Releases: 0 | Double: 0")
        
        # Style labels
        font = QFont()
        font.setPointSize(12)
        for label in [self.position_label, self.relative_label, self.button_label, 
                      self.event_label, self.stats_label]:
            label.setFont(font)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(label)
        
        central_widget.setLayout(layout)
        
        # Enable mouse tracking
        self.setMouseTracking(True)
        
    def mouseMoveEvent(self, event):
        """Track mouse movement in real-time"""
        self.move_count += 1
        pos = event.position()
        global_pos = event.globalPosition()
        
        self.position_label.setText(f"Global Position: ({global_pos.x():.1f}, {global_pos.y():.1f})")
        self.relative_label.setText(f"Relative Position: ({pos.x():.1f}, {pos.y():.1f})")
        self.event_label.setText("Event: Moving")
        self.update_stats()
    
    def mousePressEvent(self, event):
        """Track mouse button press"""
        self.click_count += 1
        button_name = self.get_button_name(event.button())
        pos = event.position()
        
        self.button_label.setText(f"Button Pressed: {button_name}")
        self.relative_label.setText(f"Relative Position: ({pos.x():.1f}, {pos.y():.1f})")
        self.event_label.setText(f"Event: {button_name} Pressed")
        self.update_stats()
    
    def mouseReleaseEvent(self, event):
        """Track mouse button release"""
        self.release_count += 1
        button_name = self.get_button_name(event.button())
        pos = event.position()
        
        self.button_label.setText(f"Button Released: {button_name}")
        self.relative_label.setText(f"Relative Position: ({pos.x():.1f}, {pos.y():.1f})")
        self.event_label.setText(f"Event: {button_name} Released")
        self.update_stats()
    
    def mouseDoubleClickEvent(self, event):
        """Track mouse double click"""
        self.double_click_count += 1
        button_name = self.get_button_name(event.button())
        pos = event.position()
        
        self.button_label.setText(f"Button Double Clicked: {button_name}")
        self.relative_label.setText(f"Relative Position: ({pos.x():.1f}, {pos.y():.1f})")
        self.event_label.setText(f"Event: {button_name} Double Clicked")
        self.update_stats()
    
    def get_button_name(self, button):
        """Convert button code to readable name"""
        if button == Qt.MouseButton.LeftButton:
            return "Left"
        elif button == Qt.MouseButton.RightButton:
            return "Right"
        elif button == Qt.MouseButton.MiddleButton:
            return "Middle"
        else:
            return "Unknown"
    
    def update_stats(self):
        """Update statistics label"""
        self.stats_label.setText(
            f"Stats - Moves: {self.move_count} | Clicks: {self.click_count} | "
            f"Releases: {self.release_count} | Double: {self.double_click_count}"
        )


app = QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()