## Angle Mapping Folder
This folder contains the angle mapping tables to convert azmuth tilt angle alpha and eleation tilt angle beta from the reflecting urface in the corresponding servomotor angles for the top and bottom servomotor.

Each file contains the table for the alpha angle of the file name and all beta angles from -60.00° up to 60.00° as a numpy file. 
For example the file "angle_map_alpha_5980.npy" contains for alpha=59.80° and all beta angles, with the first line of the file conatining the angles fop beta=-60.00° and the last line for beta=60.00° in 0.01° steps.
