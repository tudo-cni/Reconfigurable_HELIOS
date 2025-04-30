# Author: Marcel Kaudewitz
# Affiliation: TU Dortmund University, Communication Networks Institute (CNI)
# Contact: marcel.kaudewitz@tu-dortmund.de
# Date: March 3, 2025

from PySide6.QtCore import Qt, QLocale, QMimeData
from PySide6.QtWidgets import QHBoxLayout, QWidget, QDoubleSpinBox, QPushButton
from PySide6.QtGui import QDrag

# Define Orchestration Item Widget With Mouse Event Method for Drag/Drop Functionality
class Orchestration_item_widget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.item = QPushButton()
        self.layout.addWidget(self.item)  
        self.item_change_time = QDoubleSpinBox(value = 2, minimum = 0, maximum=999, suffix='s')
        self.item_change_time.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.item_change_time.setButtonSymbols(QDoubleSpinBox.NoButtons)
        self.item_change_time.setAlignment(Qt.AlignRight) 
        self.layout.addWidget(self.item_change_time)  
        self.config_values = None
        self.orchestration_active = False
    
    def mouseMoveEvent(self, e):
        # Check If Left Button of Mouse is Clicked For Drag And Drop:
        if e.buttons() == Qt.LeftButton:
            drag = QDrag(self)
            mime = QMimeData()
            drag.setMimeData(mime)
            mime.setText(self.item.text())
            drag.exec(Qt.MoveAction) 