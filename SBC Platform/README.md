## SBC Platform
This folder contains the files that need to be uploaded to the SBC Platform, along with two additional files that are not included in this folder: "servo.py" and "pca9685.py" from the "[micropython-adafruit-pca9685](https://github.com/adafruit/micropython-adafruit-pca9685)" library.

Note: The values from the three calibrated positions of each servomotor obtained during the calibration process must be included in **calibration_function.py**!

- **main.py**
    - Is executed when the SBC platform is powered on.
- **wireless_module.py**
    - Initializes the wireless module of the SBC as an access point.
- **init_pca.py**
    - Initializes the two PCA9685 and the I2C connection between the PCAs and the SBC.
- **received_data_processing.py**
    - Method to convert received data string to numerical list.
- **calibration_function.py**
    - Method to calibrate the input values based on the calibration tables from the calibration procedure.
    - Note: The values from the calibration process are included here!
- **set_angle_functions.py**
    - Methods to set the PWM value of the corresponding PCA9685 outputs in order to achieve the desired mechanical tilt of the reflecting surface.