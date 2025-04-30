# Author: Marcel Kaudewitz
# Affiliation: TU Dortmund University, Communication Networks Institute (CNI)
# Contact: marcel.kaudewitz@tu-dortmund.de
# Date: March 3, 2025

import machine
from servo import Servos

# Init PCA and I2C Connection to SBC
def init_pca():
    sdaPIN = machine.Pin(20)
    sclPIN = machine.Pin(21)
    i2c=machine.I2C(id=0, sda=sdaPIN, scl=sclPIN, freq=125000)
    devices = i2c.scan()
    if len(devices) != 0:
        print('Number of I2C devices found=',len(devices))
        for device in devices:
            print("Device Hexadecimel Address= ",hex(device))
    else:
        print("No device found")
    pca_a = Servos(i2c, address=0x40, freq=100, min_us=500, max_us=2500)
    pca_b = Servos(i2c, address=0x41, freq=100, min_us=500, max_us=2500)
    
    return pca_a, pca_b
