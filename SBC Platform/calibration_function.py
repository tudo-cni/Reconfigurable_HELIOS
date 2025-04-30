# Author: Marcel Kaudewitz
# Affiliation: TU Dortmund University, Communication Networks Institute (CNI)
# Contact: marcel.kaudewitz@tu-dortmund.de
# Date: March 3, 2025

import math

def degree_calibration(servo, servo_pos, degree):
    # Calibration Value Module Position Overview
                                           #[[ (1,1), (1,2), (1,3), (1,4)],
                                           # [ (2,1), (2,2), (2,3), (2,4)],
                                           # [ (3,1), (3,2), (3,3), (3,4)],
                                           # [( 4,1), (4,2), (4,3), (4,4)]]
    
    # Add Here Your Calibration Values For Each Servomotor and Position
    # Bottom Servomotor Calibration Values
    calibration_bottom_minus_ninety =       [[ 00.00,  00.00,  00.00,  00.00],
                                             [ 00.00,  00.00,  00.00,  00.00],
                                             [ 00.00,  00.00,  00.00,  00.00],
                                             [ 00.00,  00.00,  00.00,  00.00]]
    
    calibration_bottom_zero =               [[ 00.00,  00.00,  00.00,  00.00],
                                             [ 00.00,  00.00,  00.00,  00.00],
                                             [ 00.00,  00.00,  00.00,  00.00],
                                             [ 00.00,  00.00,  00.00,  00.00]]
    
    calibration_bottom_plus_ninety =        [[ 00.00,  00.00,  00.00,  00.00],
                                             [ 00.00,  00.00,  00.00,  00.00],
                                             [ 00.00,  00.00,  00.00,  00.00],
                                             [ 00.00,  00.00,  00.00,  00.00]]
    
    # Top Servomotor Calibration Values
    calibration_elevation_minus_ninety =    [[ 00.00,  00.00,  00.00,  00.00],
                                             [ 00.00,  00.00,  00.00,  00.00],
                                             [ 00.00,  00.00,  00.00,  00.00],
                                             [ 00.00,  00.00,  00.00,  00.00]]
    
    calibration_elevation_zero =            [[ 00.00,  00.00,  00.00,  00.00],
                                             [ 00.00,  00.00,  00.00,  00.00],
                                             [ 00.00,  00.00,  00.00,  00.00],
                                             [ 00.00,  00.00,  00.00,  00.00]]
    
    calibration_elevation_plus_ninety =     [[ 00.00,  00.00,  00.00,  00.00],
                                             [ 00.00,  00.00,  00.00,  00.00],
                                             [ 00.00,  00.00,  00.00,  00.00],
                                             [ 00.00,  00.00,  00.00,  00.00]]
    
    # Calculate Calibrated Degree Value for Uncalibrated Input Degree
    if servo_pos == 'bottom_servomotor':
        if degree == 0:
            calibrated_degree = degree + calibration_bottom_minus_ninety[servo[0] - 1][servo[1] - 1]
        elif degree > 0 and degree < 90:
            calibrated_degree = degree + calibration_bottom_minus_ninety[servo[0] - 1][servo[1] - 1] * math.pow(math.cos(math.radians(degree)),2) + calibration_bottom_zero[servo[0] - 1][servo[1] - 1] * math.pow(math.sin(math.radians(degree)),2)
        elif degree == 90:
            calibrated_degree = degree + calibration_bottom_zero[servo[0] - 1][servo[1] - 1]
        elif degree > 90 and degree < 180:
            calibrated_degree = degree + calibration_bottom_zero[servo[0] - 1][servo[1] - 1] * math.pow(math.cos(math.radians(degree - 90)),2) + calibration_bottom_plus_ninety[servo[0] - 1][servo[1] - 1] * math.pow(math.sin(math.radians(degree - 90)),2)
        elif degree == 180:
            calibrated_degree = degree + calibration_bottom_plus_ninety[servo[0] - 1][servo[1] - 1]
    elif servo_pos == 'top_servomotor':
        if degree == 0:
            calibrated_degree = degree + calibration_elevation_minus_ninety[servo[0] - 1][servo[1] - 1]
        elif degree > 0 and degree < 90:
            calibrated_degree = degree + calibration_elevation_minus_ninety[servo[0] - 1][servo[1] - 1] * math.pow(math.cos(math.radians(degree)),2) + calibration_elevation_zero[servo[0] - 1][servo[1] - 1] * math.pow(math.sin(math.radians(degree)),2)
        elif degree == 90:
            calibrated_degree = degree + calibration_elevation_zero[servo[0] - 1][servo[1] - 1]
        elif degree > 90 and degree < 180:
            calibrated_degree = degree + calibration_elevation_zero[servo[0] - 1][servo[1] - 1] * math.pow(math.cos(math.radians(degree - 90)),2) + calibration_elevation_plus_ninety[servo[0] - 1][servo[1] - 1] * math.pow(math.sin(math.radians(degree - 90)),2)
        elif degree == 180:
            calibrated_degree = degree + calibration_elevation_plus_ninety[servo[0] - 1][servo[1] - 1]

    return calibrated_degree