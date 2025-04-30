# Author: Marcel Kaudewitz
# Affiliation: TU Dortmund University, Communication Networks Institute (CNI)
# Contact: marcel.kaudewitz@tu-dortmund.de
# Date: March 3, 2025

import socket
from PySide6.QtCore import QRunnable

# Define Thread for Wireless Data Transfer
class Connectivity_runner(QRunnable):
    def __init__(self, packet_counter, config_values):
        super().__init__()
        self.packet_counter_thread = packet_counter
        self.angle_values = config_values
        
    def run(self):
        data_string = str(1) + ';' + str(self.packet_counter_thread) + ';' + str(0)
        for k in range(32):
            data_string = data_string + ';' + str(self.angle_values[k])
        data_string = data_string + '\n'
        self.connection(data_string)

    def connection(self, data_string):
        HOST = "192.168.4.1"
        PORT = 80
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((HOST, PORT))
            sock.sendall(str.encode(data_string))
            data = sock.recv(1024)