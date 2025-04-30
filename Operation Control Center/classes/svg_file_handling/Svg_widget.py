# Author: Marcel Kaudewitz
# Affiliation: TU Dortmund University, Communication Networks Institute (CNI)
# Contact: marcel.kaudewitz@tu-dortmund.de
# Date: March 3, 2025

from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter
from PySide6.QtSvg import QSvgRenderer

# Define Widget For SVG-File Display
class Svg_widget(QWidget):
    def __init__(self, svg_file):
        super().__init__()
        self.renderer = QSvgRenderer(svg_file)

    def paintEvent(self, event):
        painter = QPainter(self)
        self.renderer.render(painter)