## Content of this Repository
This repository contains the code of the operation control center and SBC platform from our paper **Field Performance Evaluation of a
Mechatronic Reflector System in a Private mmWave Network Environment**.

If you use this code, please cite our original work in [Citation](#citation).


## Repository Structure
This paragraph describes the existing folder structure of the repository.
#### Main Folder
- **reconfigurable-helios-platform/**
  - Contains all project files and subfolders.  
##### Subfolders
- **Operation Control Center**
  - Contains all necessary files to run the operation control center
  - **angle mapping**
    - Contains the tables to convert the mechanical azimuth and elevation tilt angles alpha and beta to the corresponding servomotor angles from the top and bottom servomotor
  - **classes**
    - Contains the classes and methods for the operation control center
  - **configurations**
    - Configurations from the operation control center are saved in this folder in txt-files
  - **logos**
    - Contains the svg-files of TU Dortmund University and Communication Networks Institute logos for the operation control center
  - operation_control_center.py
    - Main file of the operation control center
- **Platform Code**
  - Contains the .py files, which run on the SBC


## Quick Start
#### Operation Control Center
This repository contains the code for the Operation Control Center, developed in Python.

To run the Operation Control Center, [NumPy](https://numpy.org/), [PySide6](https://pypi.org/project/PySide6/), to provide access to the QT6.0+ framework, and the [Qt-Material](https://qt-material.readthedocs.io/en/latest/index.html) packages are required.

The code has been tested with the following versions:
- Python: 3.13.0
- Numpy: 2.1.3
- PySide6: 6.9.0
- Qt-Material: 2.14

To start the operation control center, execute **"operation_control_center.py"**.

#### SBC Platform
To run the platform code, you must upload the necessary files from the "Platform Code" folder to the Raspberry Pi Pico, along with the two files "servo.py" and "pca9685.py" from the "[micropython-adafruit-pca9685](https://github.com/adafruit/micropython-adafruit-pca9685)" library.
Please note that these two files are not included in the folder and need to be downloaded from the specified library.

The "main.py" file will then be executed automatically upon starting the single-board computer (SBC).


## Acknowledgement
This work has been supported by the German Federal Ministry of Research, Technology and Space ([BMFTR](https://https://www.bundesregierung.de/breg-en/federal-government/ministries/federal-ministry-of-research-technology-and-space)) in the course of the
[6GEM Research Hub](https://www.6gem.de/en/) under the grant number 16KISK038.

## Citation
If you use this code in any of your publications, please cite our work (author's version) as:
```
@article{Haeger/etal/2025b,
	Author = {S. H{\"a}ger, M. Kaudewitz, F. Schmickmann, S. B{\"o}cker, and C. Wietfeld},
	Title = {Field Performance Evaluation of a Mechatronic Reflector System in a Private {mmWave} Network Environment},
	Journal = {IEEE Open Journal of the Communications Society},
	Month= may, 
	Year = {2025},
	Pages = {1-24},
	Doi = {10.1109/OJCOMS.2025.3572723},
  	Note = {Early Access},
	Project = {6GEM}, 
}
```