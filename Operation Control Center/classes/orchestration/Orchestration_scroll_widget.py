# Author: Marcel Kaudewitz
# Affiliation: TU Dortmund University, Communication Networks Institute (CNI)
# Contact: marcel.kaudewitz@tu-dortmund.de
# Date: March 3, 2025

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QScrollArea, QVBoxLayout, QWidget

from .Orchestration_item_widget import Orchestration_item_widget

# Define Orchestration Beambook Widget With Scroll Functionality
class Orchestration_scroll_widget(QWidget):
    def __init__(self, main_window):
        super().__init__()
        main_layout = QVBoxLayout(self)
        self.setAcceptDrops(True)
        self.main_window = main_window
        self.last_x = None
        self.last_y = None  

        # Define Scroll Area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Container Widget for Items
        self.item_container = QWidget()
        self.item_layout = QVBoxLayout(self.item_container)
        self.item_layout.setAlignment(Qt.AlignTop)

        # Add Item Container to Main Layout and Scroll Area
        self.item_container.setLayout(self.item_layout)
        scroll_area.setWidget(self.item_container) 
        main_layout.addWidget(scroll_area)
    
    # Drag and Drop Functionality Methods
    def dragEnterEvent(self, e):
        self.last_x = e.position().x()
        self.last_y = e.position().y()
        e.accept()

    def dropEvent(self, e):
        pos = e.position()
        widget = e.source()

        # Check If Dropped Widget Is From Orchestration Mode Window:
        if isinstance(widget, Orchestration_item_widget):
            # Check If Orchestration Mode Window is Empty:
            if self.item_layout.count() == 0:
                self.item_layout.insertWidget(0, widget)
            # Else The Widget is Placed At The Position of The Drop:
            else:
                w = self.item_layout.itemAt(0).widget()
                # Position Before First Widget
                if int(pos.y()) < int(w.y() + w.size().height()/2):
                    self.item_layout.insertWidget(0, widget)
                else:
                    w = self.item_layout.itemAt(self.item_layout.count() - 1).widget()
                    # Position After Last Widget
                    if int(pos.y()) >= int(w.y() + w.size().height()/2):
                        self.item_layout.insertWidget(self.item_layout.count() - 1, widget)
                    # Else Go Through Widgets And Place Widget Inbetween Two Other Widgets
                    else:
                        if self.last_y <= e.position().y():
                            for n in range(1, self.item_layout.count()):
                                w = self.item_layout.itemAt(n).widget()
                                if int(pos.y()) < int(w.y() + w.size().height()/2):
                                    self.item_layout.insertWidget(n-1, widget)
                                    break
                        else:
                            for n in range(1, self.item_layout.count()):
                                w = self.item_layout.itemAt(n).widget()
                                if int(pos.y()) < int(w.y() + w.size().height()/2):
                                    self.item_layout.insertWidget(n, widget)
                                    break                                
        # Else The Dropped Widget is From The Beambook:
        else:
            # Check If Orchestration Mode is Empty:
            if self.item_layout.count() == 0:
                new_widget = Orchestration_item_widget()
                new_widget.item.setText(e.mimeData().text())
                new_widget.config_values = e.source().config_values
                self.item_layout.insertWidget(0, new_widget)
            # Else The Widget is Added At The Position of The Drop:
            else:
                w = self.item_layout.itemAt(0).widget()
                # Position Before First Widget
                if int(pos.y()) < int(w.y() + w.size().height()/2):
                    new_widget = Orchestration_item_widget()
                    new_widget.item.setText(e.mimeData().text())
                    new_widget.config_values = e.source().config_values
                    self.item_layout.insertWidget(0, new_widget)
                else:
                    w = self.item_layout.itemAt(self.item_layout.count() - 1).widget()
                    # Position After Last Widget
                    if int(pos.y()) >= int(w.y() + w.size().height()/2):
                        new_widget = Orchestration_item_widget()
                        new_widget.item.setText(e.mimeData().text())
                        new_widget.config_values = e.source().config_values
                        self.item_layout.insertWidget(self.item_layout.count(), new_widget)
                    # Else Go Through Widgets And Add Widget Inbetween Two Other Widgets
                    else:
                        for n in range(0, self.item_layout.count() - 1):
                            w = self.item_layout.itemAt(n).widget()
                            v = self.item_layout.itemAt(n + 1).widget()
                            if int(pos.y()) >= int(w.y() + w.size().height()/2) and int(pos.y()) < int(v.y() + v.size().height()/2):
                                new_widget = Orchestration_item_widget()
                                new_widget.item.setText(e.mimeData().text())
                                new_widget.config_values = e.source().config_values
                                self.item_layout.insertWidget(n+1, new_widget)
                                break               
            self.main_window.resizeEvent(event=0)
        self.last_x = None
        self.last_y = None
        e.accept()