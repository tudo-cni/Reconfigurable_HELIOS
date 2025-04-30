# Author: Marcel Kaudewitz
# Affiliation: TU Dortmund University, Communication Networks Institute (CNI)
# Contact: marcel.kaudewitz@tu-dortmund.de
# Date: March 3, 2025

import calibration_function

# Get PCA Index for Servomotor Input
def get_pca_index(servo):
    if servo[0] == 1 or servo[0] == 2: 
        pca_index = 0
    elif servo[0] == 3 or servo[0] == 4: 
        pca_index = 1
  
    return pca_index

# Map Module 2D-Naming Matrix to 1D-Naming From 0-15
def get_servo_index(servo):
    if servo == [1,1]:
        servo_index = 0
    elif servo == [1,2]:
        servo_index = 2
    elif servo == [1,3]:
        servo_index = 4
    elif servo == [1,4]:
        servo_index = 6
    elif servo == [2,1]:
        servo_index = 8
    elif servo == [2,2]:
        servo_index = 10
    elif servo == [2,3]:
        servo_index = 12
    elif servo == [2,4]:
        servo_index = 14
    elif servo == [3,1]:
        servo_index = 0
    elif servo == [3,2]:
        servo_index = 2       
    elif servo == [3,3]:
        servo_index = 4
    elif servo == [3,4]:
        servo_index = 6          
    elif servo == [4,1]:
        servo_index = 8
    elif servo == [4,2]:
        servo_index = 10        
    elif servo == [4,3]:
        servo_index = 12
    elif servo == [4,4]:
        servo_index = 14

    return servo_index

# Set PCA Outputs for each Servomotor
def set_pca_outputs(received_degrees, pca_a, pca_b):
    # Normalize Data from range (-90,90) to (0,180)
    for k in range(3,len(received_degrees)):
        received_degrees[k] = received_degrees[k] + 90
    # Check If Values Should Be Calibrated
    if received_degrees[0] == 1:
        k = 3
        for n in range(1,5):
            for m in range(1,5):
                received_degrees[k] = calibration_function.degree_calibration((n,m),'bottom_servomotor',received_degrees[k])
                received_degrees[k+1] = calibration_function.degree_calibration((n,m),'top_servomotor',received_degrees[k+1])
                k = k + 2
    # Set Degree Values At PCA
    k = 3
    for n in range(1,5):
        for m in range(1,5):
            pca_index = get_pca_index([n,m])
            servo_index = get_servo_index([n,m])
            # Distinguish Between the Two PCAs
            if pca_index == 0:
                pca_a.position(servo_index, degrees=received_degrees[k])
                pca_a.position(servo_index + 1, degrees=received_degrees[k + 1])
            elif pca_index == 1:
                pca_b.position(servo_index, degrees=received_degrees[k])
                pca_b.position(servo_index + 1, degrees=received_degrees[k + 1])
                
# Release All PCA Outputs to None
def pca_release_all(pca_a, pca_b):
    for n in range(1,5):
        for m in range(1,5):
            pca_index = get_pca_index([n,m])
            servo_index = get_servo_index([n,m])
            # Distinguish Between the Two PCAs
            if pca_index == 0:
                pca_a.release(servo_index)
                pca_a.release(servo_index + 1)     
            elif pca_index == 1:
                pca_b.release(servo_index)
                pca_b.release(servo_index + 1)  