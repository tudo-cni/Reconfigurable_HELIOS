# Author: Marcel Kaudewitz
# Affiliation: TU Dortmund University, Communication Networks Institute (CNI)
# Contact: marcel.kaudewitz@tu-dortmund.de
# Date: March 3, 2025

from PySide6.QtCore import Signal, QObject

# Define Orchestration Timer Thread and Signal
class Finished_signal(QObject):
    finished = Signal(int)