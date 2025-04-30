# Author: Marcel Kaudewitz
# Affiliation: TU Dortmund University, Communication Networks Institute (CNI)
# Contact: marcel.kaudewitz@tu-dortmund.de
# Date: March 3, 2025

import os

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QScrollArea, QVBoxLayout, QWidget

from .Beambook_item_widget import Beambook_item_widget

# Hardcoded Configurations (Expandable):
CONFIGS_NAMES = ['NEUTRAL']
CONFIG_VALUES = [[    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0]] # NEUTRAL

# Define Beam Codebook Widget With Scroll Functionality
class Beambook_scroll_widget(QWidget):
    def __init__(self):
        super().__init__()
        main_layout = QVBoxLayout(self)
        self.setAcceptDrops(True)

        # Define Scroll Area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Container Widget for Items
        self.item_container = QWidget()
        self.item_layout = QVBoxLayout(self.item_container)
        self.item_layout.setAlignment(Qt.AlignTop)

        # Load Hardcoded Configurations
        initial_count = 0
        # Go Through Hardcoded Configurations:
        for k in CONFIGS_NAMES:
            new = Beambook_item_widget()
            new.item.setText(CONFIGS_NAMES[initial_count])
            new.config_values = CONFIG_VALUES[initial_count]
            self.item_layout.addWidget(new)
            initial_count += 1
        
        # Load Configurations from Configuration Folder
        initial_count = 0
        directory = os.path.join(os.path.dirname(__file__),'..','..','configurations')
        filenames = next(os.walk(directory), (None, None, []))[2]
        # Go Through All Files(Configurations) Saved in Configurations Folder:
        for path in os.listdir(directory):
            # Check If File Exist And is Not Readme File:
            if os.path.isfile(os.path.join(directory, path)) and filenames[initial_count].split('.')[0] != 'Readme':
                new = Beambook_item_widget()
                with open(os.path.join(directory, filenames[initial_count]), mode = 'r') as file:
                    temp_data = file.read().split(';')
                    temp_data_numbers = []
                    # Go Through Data String From File:
                    for k in range(0,len(temp_data)):
                        temp_data_numbers.append(float(temp_data[k]))
                    new.config_values = temp_data_numbers
                new.item.setText(filenames[initial_count].split('.')[0])
                self.item_layout.addWidget(new)
                initial_count += 1

        # Add Item Container to Main Layout and Scroll Area
        self.item_container.setLayout(self.item_layout)
        scroll_area.setWidget(self.item_container) 
        main_layout.addWidget(scroll_area)
    
    # Drag and Drop Functionality Methods
    def dragEnterEvent(self, e):
        e.accept()

    def dropEvent(self, e):
        pos = e.position()
        widget = e.source()
        # Check If Dropped Widget is Not a Beambook Widget:
        if not isinstance(widget, Beambook_item_widget):
            widget.deleteLater()  
        e.accept()