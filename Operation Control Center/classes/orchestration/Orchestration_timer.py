# Author: Marcel Kaudewitz
# Affiliation: TU Dortmund University, Communication Networks Institute (CNI)
# Contact: marcel.kaudewitz@tu-dortmund.de
# Date: March 3, 2025

import time

from PySide6.QtCore import Signal, QRunnable, QObject

# Define Orchestration Timer Thread and Signal
class Finished_signal(QObject):
    finished = Signal(int)

class Orchestration_timer(QRunnable):
    def __init__(self, main_window, time):
        super().__init__()
        self.time_value = time
        self.pause = False
        self.reset = False
        self.finished_signal = Finished_signal()
        self.main_window = main_window
    
    def run(self):
        counter = int(self.time_value*100)
        reset = 0
        # While Counter >0 Wait (Sleep):
        while counter > 0:
            time.sleep(0.01)
            counter = counter - 1
            if self.pause:
                time.sleep(0.10)
            if self.reset:
                reset = 1
                break
        self.finished_signal.finished.emit(reset) 