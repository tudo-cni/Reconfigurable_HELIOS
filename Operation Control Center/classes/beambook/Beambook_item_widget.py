# Author: Marcel Kaudewitz
# Affiliation: TU Dortmund University, Communication Networks Institute (CNI)
# Contact: marcel.kaudewitz@tu-dortmund.de
# Date: March 3, 2025

from PySide6.QtCore import Qt, QMimeData
from PySide6.QtWidgets import QHBoxLayout, QWidget, QPushButton
from PySide6.QtGui import QDrag

# Define Beambook Item Widget With Mouse Event Method for Drag/Drop Functionality
class Beambook_item_widget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.item = QPushButton()
        self.layout.addWidget(self.item)   
        self.config_values = None

    def mouseMoveEvent(self, e):
        # Check If Left Button of Mouse is Clicked For Drag And Drop:
        if e.buttons() == Qt.LeftButton:
            drag = QDrag(self)
            mime = QMimeData()
            mime.setText(self.item.text())
            drag.setMimeData(mime)
            drag.exec(Qt.MoveAction) 