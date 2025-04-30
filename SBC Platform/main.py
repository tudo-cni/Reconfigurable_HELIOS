# Author: Marcel Kaudewitz
# Affiliation: TU Dortmund University, Communication Networks Institute (CNI)
# Contact: marcel.kaudewitz@tu-dortmund.de
# Date: March 3, 2025

import machine
import time

import wireless_module
import init_pca
import set_angle_functions
import received_data_processing


# Init Wireless Module and Server Socket
wireless_module.init_wireless_module()
server = wireless_module.start_server()
  
# Init PCAs
pca_a, pca_b = init_pca.init_pca()

# Init Pi LED
led = machine.Pin("LED", machine.Pin.OUT)
temp_packet_number = 0
set_angle_functions.set_pca_outputs([1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], pca_a, pca_b)

time.sleep(1.0)
set_angle_functions.pca_release_all(pca_a, pca_b)

# Set LED ON, Pi Ready
led.on()

# Listen On Connection, Wait For Input By Operation Control
while True:
    try:
        conn, byte_data = wireless_module.server_listen(server)
        received_degrees = received_data_processing.data_processing(byte_data)     
        if received_degrees[1] >= temp_packet_number or received_degrees[1] == 0:
            set_angle_functions.set_pca_outputs(received_degrees, pca_a, pca_b)
            temp_packet_number = received_degrees[1]
        conn.send(b'OK')
        conn.close()
        print('Connection closed')
        print()
        print('Finished')
        
    except OSError as e:
        break
    except (KeyboardInterrupt):
        break

try: conn.close()
except NameError: pass
server.close()


                    
    



