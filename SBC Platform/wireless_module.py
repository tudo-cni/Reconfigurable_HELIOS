# Author: Marcel Kaudewitz
# Affiliation: TU Dortmund University, Communication Networks Institute (CNI)
# Contact: marcel.kaudewitz@tu-dortmund.de
# Date: March 3, 2025

import network, rp2, time
import socket

def init_wireless_module():
    rp2.country('DE')
    wap = network.WLAN(network.AP_IF)
    wap.config(essid='ReconfigurableHELIOS', password='12345678')
    wap.active(True)

    
def start_server():
    print('Start Server')
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(addr)
    server.listen(1)

    return server

def server_listen(server):
    conn, addr = server.accept()
    request = conn.recv(1024)

    return conn, request

    