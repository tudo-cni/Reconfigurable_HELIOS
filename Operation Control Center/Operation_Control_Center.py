# Author: Marcel Kaudewitz
# Affiliation: TU Dortmund University, Communication Networks Institute (CNI)
# Contact: marcel.kaudewitz@tu-dortmund.de
# Date: March 3, 2025

import sys, os, time, math
import numpy as np
from PySide6.QtCore import Qt, QThreadPool, QLocale
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QGridLayout, QWidget, QDoubleSpinBox, QPushButton, QCheckBox, QButtonGroup, QFileDialog
from PySide6.QtGui import QIcon
from qt_material import apply_stylesheet

from classes.svg_file_handling.Svg_widget import Svg_widget
from classes.beambook.Beambook_item_widget import Beambook_item_widget
from classes.beambook.Beambook_scroll_widget import Beambook_scroll_widget
from classes.orchestration.Orchestration_item_widget import Orchestration_item_widget
from classes.orchestration.Orchestration_scroll_widget import Orchestration_scroll_widget
from classes.orchestration.Orchestration_timer import Orchestration_timer
from classes.connection_handling.Connectivity_runner import Connectivity_runner

# Main Window
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        # Set Window Logo and Titel
        icon = QIcon("logos/LogoTUDO_small.svg")
        self.setWindowIcon(icon)
        self.setWindowTitle("R-HELIOS | TU Dortmund University | Communication Networks Institute")

        # Define Variables for Orchestration/Connectivity and Thread Handling
        self.threadpool = QThreadPool()
        self.orchestration_counter = 0
        self.orchestration_worker = None
        self.connection_worker = None
        self.session_packet_counter = 0
        self.configuration_send = None

        # Define Main Widget and Grid Layout With Number of Rows and Columns:
        self.widget = QWidget()
        self.layout = QGridLayout()
        self.setAcceptDrops(True)
        self.number_rows_main_grid = 74
        self.number_columns_main_grid = 51
        # Equal Stretch Factors for Each Row/Column
        for i in range(self.number_rows_main_grid):
            self.layout.setRowStretch(i, 1)
        for j in range(self.number_columns_main_grid):
            self.layout.setColumnStretch(j, 1)

        # Define/Add Widgets 
        # Define/Add Logos and Title
        self.tu_logo_widget = Svg_widget("logos/LogoTUDO.svg")
        self.layout.addWidget(self.tu_logo_widget, 0, 1, 5, 15)
        self.titel_label = QLabel("Orchestration Center")
        self.layout.addWidget(self.titel_label,3,int(self.number_columns_main_grid/2-12.5),2,25)
        self.subtitel_label = QLabel("Reconfigurable HELIOS Reflector")
        self.layout.addWidget(self.subtitel_label,0,int(self.number_columns_main_grid/2-12.5),3,25)
        self.cni_logo_widget = Svg_widget("logos/LogoCNI.svg") 
        self.layout.addWidget(self.cni_logo_widget, 0, self.number_columns_main_grid-6, 5, 5)
        # Define/Add Seperator Line 1
        self.separator_label_1 = QLabel()
        self.separator_label_1.setStyleSheet("background-color: #85b818;")
        self.layout.addWidget(self.separator_label_1,5,1,1,self.number_columns_main_grid-2)
        # Define/Add Direct Angle Input Elements
        self.direct_input_label = QLabel("Manual Beambook Entry Configuration")
        self.layout.addWidget(self.direct_input_label, 6, 0, 2, self.number_columns_main_grid)
        self.direct_input_module_labels = []
        self.direct_input_module_azimuth_value_box = []
        self.direct_input_module_elevation_value_box = []
        self.direct_input_module_phi_label = []
        self.direct_input_module_theta_label = []
        self.direct_input_module_checkbox = []
        # Go Through Module Rows:
        for k in range(4):
            # Go Through Module Columns:
            for l in range(4):
                # Define Module QLabels and Add to Layout:
                self.direct_input_module_labels.append(QLabel(f'{k+1},{l+1}'))        
                self.direct_input_module_labels[k*4+l].setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
                self.layout.addWidget(self.direct_input_module_labels[k*4+l],15-k*5+8,l*12+l,2,6)  
                # Define Modules Azimuth and Evaluation QDoubleSpinBoxes and Add to Layout
                self.direct_input_module_azimuth_value_box.append(QDoubleSpinBox(minimum=-60,maximum=60,suffix='°'))
                self.direct_input_module_azimuth_value_box[k*4+l].setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
                self.direct_input_module_azimuth_value_box[k*4+l].setButtonSymbols(QDoubleSpinBox.NoButtons)
                self.direct_input_module_azimuth_value_box[k*4+l].setAlignment(Qt.AlignRight) 
                self.layout.addWidget(self.direct_input_module_azimuth_value_box[k*4+l],15-k*5+10,l*12+l,3,6)  
                self.direct_input_module_elevation_value_box.append(QDoubleSpinBox(minimum=-60,maximum=60,suffix='°'))
                self.direct_input_module_elevation_value_box[k*4+l].setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
                self.direct_input_module_elevation_value_box[k*4+l].setButtonSymbols(QDoubleSpinBox.NoButtons)
                self.direct_input_module_elevation_value_box[k*4+l].setAlignment(Qt.AlignRight) 
                self.layout.addWidget(self.direct_input_module_elevation_value_box[k*4+l],15-k*5+10,l*12+6+l,3,6)  
                # Define Labels for Phi and Theta
                self.direct_input_module_phi_label.append(QLabel(' ' + '\u03b1'))
                self.direct_input_module_phi_label[k*4+l].setAttribute(Qt.WA_TransparentForMouseEvents)
                self.direct_input_module_phi_label[k*4+l].setStyleSheet('QLabel {color: #949494}')
                self.direct_input_module_phi_label[k*4+l].setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
                self.layout.addWidget(self.direct_input_module_phi_label[k*4+l],15-k*5+10,l*12+l,3,2)  
                self.direct_input_module_theta_label.append(QLabel(' ' + '\u03B2'))
                self.direct_input_module_theta_label[k*4+l].setAttribute(Qt.WA_TransparentForMouseEvents)
                self.direct_input_module_theta_label[k*4+l].setStyleSheet('QLabel {color: #949494}')
                self.direct_input_module_theta_label[k*4+l].setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
                self.layout.addWidget(self.direct_input_module_theta_label[k*4+l],15-k*5+10,l*12+6+l,3,2) 
                # Define QCheckBoxes
                self.direct_input_module_checkbox.append(QCheckBox())
                self.layout.addWidget(self.direct_input_module_checkbox[k*4+l],15-k*5+8,l*12+l+8,2,4)
        self.direct_input_button_select_all = QPushButton('Select All')
        self.direct_input_button_select_all.clicked.connect(self.set_angles_button_select_all_clicked)
        self.layout.addWidget(self.direct_input_button_select_all,28,26,3,12)
        self.direct_input_button_unselect_all = QPushButton('Unselect All')
        self.direct_input_button_unselect_all.clicked.connect(self.set_angles_button_unselect_all_clicked)
        self.layout.addWidget(self.direct_input_button_unselect_all,28,39,3,12)
        self.set_configuration_button = QPushButton("Set\nConfiguration")
        self.set_configuration_button.clicked.connect(self.set_configuration_button_clicked)
        self.layout.addWidget(self.set_configuration_button, 28,0,4,12)
        self.save_configuration_button = QPushButton('Save\nConfiguration')
        self.save_configuration_button.clicked.connect(self.save_configuration)
        self.layout.addWidget(self.save_configuration_button,28,13,4,12)
        # Define/Add Seperator Line 2
        self.separator_label_2 = QLabel()
        self.separator_label_2.setStyleSheet("background-color: #85b818;")
        self.layout.addWidget(self.separator_label_2,33,1,1,self.number_columns_main_grid-2)  
        # Define/Add IRS Beam Codebook 
        self.beambook_label = QLabel("IRS Beam Codebook")
        self.layout.addWidget(self.beambook_label, 34, 0, 2, 23)
        self.beambook_widget = Beambook_scroll_widget()
        self.layout.addWidget(self.beambook_widget, 35, 0, 26, 23)
        # Define/Add Switching Orchestration
        self.switching_orchestration_label = QLabel("Beam Switching Orchestration")
        self.layout.addWidget(self.switching_orchestration_label, 34, 23, 2, 25)
        self.orchestration_widget = Orchestration_scroll_widget(self)
        self.layout.addWidget(self.orchestration_widget, 35, 24, 23, 28)
        self.start_orchestration_btn = QPushButton('Start')
        self.start_orchestration_btn.clicked.connect(lambda: self.orchestration_mode(-1))
        self.layout.addWidget(self.start_orchestration_btn,57,26,3,12)
        self.reset_orchestration_btn = QPushButton('Reset')
        self.reset_orchestration_btn.clicked.connect(self.orchestration_mode_reset)
        self.layout.addWidget(self.reset_orchestration_btn,57,39,3,12)
        # Define/Add Seperator Line 3
        self.separator_label_3 = QLabel()
        self.separator_label_3.setStyleSheet("background-color: #85b818;")
        self.layout.addWidget(self.separator_label_3,62,1,1,self.number_columns_main_grid-2) 
        # Define/Add Geometry Configuration Calculation
        self.geometry_label = QLabel("Configuration Calculation for Scenario Geometry")
        self.layout.addWidget(self.geometry_label, 63, 0, 2, 51)
        self.geometry_input = []
        for l in range(2):
            for k in range(3):
                self.geometry_input.append(QDoubleSpinBox(minimum=-99.99,maximum=99.99,suffix='m'))
                self.geometry_input[k+l*3].setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
                self.geometry_input[k+l*3].setButtonSymbols(QDoubleSpinBox.NoButtons)
                self.geometry_input[k+l*3].setAlignment(Qt.AlignRight) 
                self.layout.addWidget(self.geometry_input[k+l*3],65+k*3,19+13*l,3,6)
        self.calculate_configuration_btn = QPushButton("Calculate\nConfiguration")
        self.calculate_configuration_btn.clicked.connect(self.geometry_configuration_calculation)
        self.layout.addWidget(self.calculate_configuration_btn, 70, 0, 4, 12)
        self.bs_label = QLabel("BS:")
        self.layout.addWidget(self.bs_label,65,29,3,3)
        self.ue_label = QLabel("UE:")
        self.layout.addWidget(self.ue_label,65,16,3,3)       
        self.coordinate_labels = []
        for k in range(2):
            self.coordinate_labels.append(QLabel("x"))
            self.coordinate_labels.append(QLabel("y"))
            self.coordinate_labels.append(QLabel("z"))
        for k in range(6):
            self.coordinate_labels[k].setAttribute(Qt.WA_TransparentForMouseEvents)
            self.coordinate_labels[k].setStyleSheet('QLabel {color: #949494}')
            self.coordinate_labels[k].setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        for l in range(2):
            for k in range(3):
                self.layout.addWidget(self.coordinate_labels[k+l*3],65+k*3,19+13*l,3,6)
        self.calculation_method_checkbox_group = QButtonGroup()
        self.calculation_method_checkbox_group.setExclusive(True)        
        self.individually_config_checkbox = QCheckBox()
        self.calculation_method_checkbox_group.addButton(self.individually_config_checkbox)
        self.individually_config_checkbox.setCheckState(Qt.CheckState.Checked)
        self.layout.addWidget(self.individually_config_checkbox,65,0,2,4)
        self.equally_config_checkbox = QCheckBox()
        self.calculation_method_checkbox_group.addButton(self.equally_config_checkbox)
        self.layout.addWidget(self.equally_config_checkbox,67,0,2,4)
        self.individually_config_label = QLabel("Individually Aligned")
        self.layout.addWidget(self.individually_config_label,65,2,2,12)
        self.equally_config_label = QLabel("Equally Aligned")
        self.layout.addWidget(self.equally_config_label,67,2,2,12)
        self.intermodule_spacing_label = QLabel("Intermodule Spacing:")
        self.layout.addWidget(self.intermodule_spacing_label,65,39,3,12)
        self.intermodule_spacing_input = []
        for k in range(2):
            self.intermodule_spacing_input.append(QDoubleSpinBox())
            self.intermodule_spacing_input[k].setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
            self.intermodule_spacing_input[k].setButtonSymbols(QDoubleSpinBox.NoButtons)
            self.intermodule_spacing_input[k].setSuffix('m')
            self.intermodule_spacing_input[k].setAlignment(Qt.AlignRight) 
            self.intermodule_spacing_input[k].setMinimum(-1) 
            self.intermodule_spacing_input[k].setMaximum(1) 
            self.layout.addWidget(self.intermodule_spacing_input[k],68+k*3,45,3,6)
        self.delta_y_label = QLabel('\u0394y')
        self.delta_y_label.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.delta_y_label.setStyleSheet('QLabel {color: #949494}')
        self.delta_y_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.layout.addWidget(self.delta_y_label,68,45,3,6)   
        self.delta_z_label = QLabel('\u0394z')
        self.delta_z_label.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.delta_z_label.setStyleSheet('QLabel {color: #949494}')
        self.delta_z_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.layout.addWidget(self.delta_z_label,71,45,3,6)   
        
        # Set Central Widget and Main Layout
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)
        self.setMinimumSize(self.number_columns_main_grid*11, self.number_rows_main_grid*10) 

    # Methods for Drop/Load From Beambook Functionality 
    def dragEnterEvent(self, e):
        e.accept()
    
    def dropEvent(self, e):
        height = self.height()/self.number_rows_main_grid
        widget = e.source()
        # Check If Dragged Widget is From Beambook
        if isinstance(widget,Beambook_item_widget):
            # Check If Beambook Widget Drop Position is on the Manual Beam Entry Area to Load Widget
            if e.position().y() >= 8*height and e.position().y() <= 28*height:
                for k in range(16):
                    self.direct_input_module_azimuth_value_box[k].setValue(widget.config_values[k*2])
                    self.direct_input_module_elevation_value_box[k].setValue(widget.config_values[k*2+1])
        # Else Delete Dragged Widget
        else:
            widget.deleteLater()
        e.accept()

    # Method for 'SET CONFIGURATION' - Sending Configuration to R-HELIOS
    def set_configuration_button_clicked(self):
        # Check If Automatic Orchestration is Deactive:
        if self.orchestration_counter == 0:
            self.configuration_send = []
            # Go Through The 16 Alpha And Beta Angles:
            for k in range(16):
                alpha, beta = self.helios_to_servo_angles(self.direct_input_module_azimuth_value_box[k].value(),self.direct_input_module_elevation_value_box[k].value())
                self.configuration_send.append(alpha)
                self.configuration_send.append(beta)
            self.connection_worker = Connectivity_runner(self.session_packet_counter,self.configuration_send)
            self.session_packet_counter = self.session_packet_counter + 1
            self.connection_worker.setAutoDelete(True)
            self.threadpool.start(self.connection_worker)
    
    # Method for 'SELECT ALL' Button - Check All Checkboxes
    def set_angles_button_select_all_clicked(self):
        # Go Through The 16 Module Checkboxes
        for k in range(0,16):
            self.direct_input_module_checkbox[k].setCheckState(Qt.CheckState.Checked)
    
    # Method for 'UNSELECT ALL' Button - Uncheck All Checkboxes
    def set_angles_button_unselect_all_clicked(self):
        # Go Through The 16 Module Checkboxes
        for k in range(0,16):
            self.direct_input_module_checkbox[k].setCheckState(Qt.CheckState.Unchecked)
    
    # Method for Calculating the Configuration From Geometry Input 
    def geometry_configuration_calculation(self):
        # Go Through Module Rows:
        for k in range(4):
            # Go Through Module Columns:
            for l in range(4):
                # Check If Module Checkbox is Checked:
                if self.direct_input_module_checkbox[k*4+l].isChecked():
                    # Check If Individually Aligned Configuration Should be Calculated For Module:
                    if self.individually_config_checkbox.isChecked():
                        alpha,beta = self.calculate_angles(-self.intermodule_spacing_input[0].value()*(3/2)+self.intermodule_spacing_input[0].value()*l,self.intermodule_spacing_input[1].value()*(3/2)-self.intermodule_spacing_input[1].value()*k)
                    # Else Calculate Equally Aligned Configuration For Module:
                    else:
                        alpha,beta = self.calculate_angles(0,0) 
                    self.direct_input_module_azimuth_value_box[k*4+l].setValue(alpha)
                    self.direct_input_module_elevation_value_box[k*4+l].setValue(beta)
    
    def calculate_angles(self,intermodule_spacing_y,intermodule_spacing_z):
        # Define Reflection Center Point
        reflection_center_point = np.zeros(3)
        reflection_center_point[0] = 0
        reflection_center_point[1] = 0 + intermodule_spacing_y
        reflection_center_point[2] = 0 + intermodule_spacing_z
        # Define R-HELIOS Normal Vector
        helios_normal_vector = np.zeros(3)
        helios_normal_vector[0] = 1
        helios_normal_vector[1] = 0       
        helios_normal_vector[2] = 0
        # Shift Coordinate System Origin to Reflection Center Point
        ue_coordinates_adjusted = np.zeros(3)
        ue_coordinates_adjusted[0] = self.geometry_input[0].value() - reflection_center_point[0]
        ue_coordinates_adjusted[1] = self.geometry_input[1].value() - reflection_center_point[1]
        ue_coordinates_adjusted[2] = self.geometry_input[2].value() - reflection_center_point[2]
        bs_coordinates_adjusted = np.zeros(3)
        bs_coordinates_adjusted[0] = self.geometry_input[3].value() - reflection_center_point[0]
        bs_coordinates_adjusted[1] = self.geometry_input[4].value() - reflection_center_point[1]
        bs_coordinates_adjusted[2] = self.geometry_input[5].value() - reflection_center_point[2]
        reflection_center_point = np.zeros(3)
        # Transform Coordinates to Spherical Coordinates
        transmitter_r = math.sqrt(bs_coordinates_adjusted[0]**2 + bs_coordinates_adjusted[1]**2 + bs_coordinates_adjusted[2]**2)
        transmitter_theta = math.acos(bs_coordinates_adjusted[2]/transmitter_r) * 180/np.pi
        transmitter_phi = math.atan2(bs_coordinates_adjusted[1],bs_coordinates_adjusted[0]) * 180/np.pi
        helios_r = math.sqrt(helios_normal_vector[0]**2 + helios_normal_vector[1]**2 + helios_normal_vector[2]**2)
        helios_theta = math.acos(helios_normal_vector[2]/helios_r) * 180/np.pi
        helios_phi = math.atan2(helios_normal_vector[1],helios_normal_vector[0]) * 180/np.pi
        receiver_r = math.sqrt(ue_coordinates_adjusted[0]**2 + ue_coordinates_adjusted[1]**2 + ue_coordinates_adjusted[2]**2)
        receiver_theta = math.acos(ue_coordinates_adjusted[2]/receiver_r) * 180/np.pi
        receiver_phi = math.atan2(ue_coordinates_adjusted[1],ue_coordinates_adjusted[0]) * 180/np.pi
        # Calculate Desired Module Angle Alpha and Beta
        diff_theta = transmitter_theta - (transmitter_theta - receiver_theta)/2
        diff_phi = transmitter_phi - (transmitter_phi - receiver_phi)/2
        rot_theta = helios_theta - diff_theta
        rot_phi = helios_phi - diff_phi
        helios_normal_vector = [0, 0, 0]
        helios_normal_vector[0] = (helios_r * math.sin((rot_theta+90) * math.pi/180) * math.cos((rot_phi) * math.pi/180))
        helios_normal_vector[1] = (helios_r * math.sin((rot_theta+90) * math.pi/180) * math.sin((rot_phi) * math.pi/180))
        helios_normal_vector[2] = (helios_r * math.cos((rot_theta+90) * math.pi/180))
        alpha_calculated = math.atan(helios_normal_vector[1]/helios_normal_vector[0]) * 180/math.pi
        beta_calculated = math.atan(helios_normal_vector[2]/helios_normal_vector[0]) * 180/math.pi     
        return alpha_calculated, beta_calculated
    
    # Method to Save Configuration in txt-File and Refresh Beam Codebook
    def save_configuration(self):
        dlg = QFileDialog()
        dlg.setNameFilter('Configuration (*.txt)')
        filename = dlg.getSaveFileName(self, "Save Configuration", os.path.join(os.path.dirname(__file__), 'configurations'), filter=('Configurations (*.txt)'))
        data_string = str(self.direct_input_module_azimuth_value_box[0].value()) + ';' + str(self.direct_input_module_elevation_value_box[0].value())
        # Go Through The 16 Alpha And Beta Angle Input Boxes:
        for k in range(1,16):
            data_string = data_string + ';' + str(self.direct_input_module_azimuth_value_box[k].value()) + ';' + str(self.direct_input_module_elevation_value_box[k].value())
        # Check That Filename is Not Empty:
        if filename[0] != '' :
            with open(filename[0], mode = 'w') as file:
                file.write(data_string)
        self.beambook_widget = Beambook_scroll_widget()     
        self.layout.addWidget(self.beambook_widget, 35, 0, 26, 23)
        self.resizeEvent(event=0)
   
    # Methods to Handle Automatic Orchestration
    def orchestration_mode(self,mode):
        # Check If Start Orchestration Button is Clicked, Method is Called With mode == -1:
        if mode == -1:
            # Check If Button Text is "Start":
            if self.start_orchestration_btn.text() == "Start":
                # Check If The Orchestration Mode was Paused And Should Continue:
                if isinstance(self.orchestration_worker, Orchestration_timer):
                    self.orchestration_worker.pause = False
                # Else The Orchestration Mode Was Deactive And is Started:
                else:
                    # Check If Number of Configurations in Orchestration Mode Window is >0:
                    if self.orchestration_widget.item_layout.count() > 0:
                        self.start_orchestration_btn.setText('Pause')
                        # Check If Orchestration Mode is Deactive And Can be Started With First Configuration:
                        if self.orchestration_counter == 0:
                            self.orchestration_counter = 1
                            self.orchestration_mode_start_item(0)
            # Else Button Text is "Pause":
            else:
                self.start_orchestration_btn.setText('Start')
                # Check If a Timer For The Configuration Holding Duration is Already Active:
                if isinstance(self.orchestration_worker, Orchestration_timer):
                    self.orchestration_worker.pause = True
        # Check If Orchestration Mode is Active and Should Continue, Method is Called With mode == 0:
        elif mode == 0:
            # Go Through All Configurations in Orchestration Mode Window:
            for k in range(self.orchestration_widget.item_layout.count()):
                # Check if The Selected Configuration is Active:
                if self.orchestration_widget.item_layout.itemAt(k).widget().orchestration_active:
                    self.orchestration_widget.item_layout.itemAt(k).widget().orchestration_active = False
                    self.orchestration_widget.item_layout.itemAt(k).widget().item.setStyleSheet(f"font: {int(min(self.width()//50, self.height()//50)/1.25)}px; border: {int(min(self.width()//50, self.height()//50)/10)}px solid #8bc34a; background-color: #31363b")
                    # Check If The Active Configuration is The Last One (Therefore Switch Back to Beginning):
                    if k == self.orchestration_widget.item_layout.count() - 1:
                        self.orchestration_mode_start_item(0)
                        self.orchestration_counter = 0
                        break
                    # Else Continue Go Through
                    else:
                        self.orchestration_mode_start_item(k+1)
                        self.orchestration_counter = self.orchestration_counter + 1
                        break
                # Else The Configuration is Deactive:
                else:
                    # Check If The Deactive Configuration is The Last One And Therefore No Active Configuration is Existing:
                    if k == self.orchestration_widget.item_layout.count() - 1:
                        self.orchestration_mode_start_item(self.orchestration_counter)
        # Else End Orchestration Mode
        else:
            # Go Through All Configurations in Orchestration Mode Window:
            for k in range(self.orchestration_widget.item_layout.count()):
                # Check if The Selected Configuration is Active:
                if self.orchestration_widget.item_layout.itemAt(k).widget().orchestration_active:
                    self.orchestration_widget.item_layout.itemAt(k).widget().orchestration_active = False
                    self.orchestration_widget.item_layout.itemAt(k).widget().item.setStyleSheet(f"font: {int(min(self.width()//50, self.height()//50)/1.25)}px; border: {int(min(self.width()//50, self.height()//50)/10)}px solid #8bc34a; background-color: #31363b")
            self.orchestration_counter = 0
    
    def orchestration_mode_start_item(self, item_position):
        self.orchestration_widget.item_layout.itemAt(item_position).widget().orchestration_active = True
        self.configuration_send = []
        # Go Through The 16 Alpha And Beta Angles:
        for k in range(16):
            alpha, beta = self.helios_to_servo_angles(self.orchestration_widget.item_layout.itemAt(item_position).widget().config_values[k*2],self.orchestration_widget.item_layout.itemAt(item_position).widget().config_values[k*2+1])
            self.configuration_send.append(alpha)
            self.configuration_send.append(beta)
        self.connection_worker = Connectivity_runner(self.session_packet_counter,self.configuration_send)
        self.session_packet_counter = self.session_packet_counter + 1
        self.connection_worker.setAutoDelete(True)
        self.threadpool.start(self.connection_worker)
        self.orchestration_widget.item_layout.itemAt(item_position).widget().item.setStyleSheet(f"font: {int(min(self.width()//50, self.height()//50)/1.25)}px; border: {int(min(self.width()//50, self.height()//50)/10)}px solid #8bc34a; background-color: #639A00")
        self.orchestration_worker = Orchestration_timer(self, self.orchestration_widget.item_layout.itemAt(item_position).widget().item_change_time.value())
        self.orchestration_worker.setAutoDelete(True)
        self.threadpool.start(self.orchestration_worker)
        self.orchestration_worker.finished_signal.finished.connect(self.orchestration_mode)
    
    def orchestration_mode_reset(self):
        self.start_orchestration_btn.setText('Start')
        self.orchestration_counter = 0
        # Check If a Timer For The Configuration Holding Duration is Active:
        if isinstance(self.orchestration_worker, Orchestration_timer):
            self.orchestration_worker.reset = True
    
    # Method to Map R-HELIOS Angles to Servomotor Angles
    def helios_to_servo_angles(self, alpha, beta):
        angle_map = np.load(f'angle mapping/angle_map_alpha_{int(alpha*100)}.npy')
        alpha_servo = angle_map[int(beta*100 + 6000)]
        beta_servo = angle_map[int(-beta*100 + 6000) + 12001]
        return alpha_servo, beta_servo

    # Methods to Toggle Fullscreen With Key F9
    def keyPressEvent(self, event):
        # Check If The Key F9 Was Pressed:
        if event.key() == Qt.Key_F9:  
            self.toggle_fullscreen()
    
    def toggle_fullscreen(self):
        # Check If Window is Already Fullscreen View:
        if self.isFullScreen():
            self.showNormal()  
            self.resize(self.number_columns_main_grid*10,self.number_rows_main_grid*10)  
        # Else The Window is in Normal View:
        else:
            self.showFullScreen()  
    
    # Method to Handle Resizing for Each Element
    def resizeEvent(self, event):  
        # Calculate Adjusted Sizes From Window Size
        width = self.width()
        height = self.height()
        grid_cell_width = width // self.number_columns_main_grid   
        grid_cell_height = height // self.number_rows_main_grid  
        for k in range(self.number_rows_main_grid):
            self.layout.setRowMinimumHeight(k,grid_cell_height)
        for k in range(self.number_columns_main_grid):
            self.layout.setColumnMinimumWidth(k,grid_cell_width)
        new_font_size = min(width // 50, height // 50)
        cell_size = min(grid_cell_height,grid_cell_width)
        # Resize Titel and Logos
        self.tu_logo_widget.setFixedSize(cell_size*15,cell_size*5)
        self.titel_label.setStyleSheet(f"font: bold {new_font_size * 1.2}px;")
        self.titel_label.setFixedHeight(cell_size*2)
        self.titel_label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.subtitel_label.setStyleSheet(f"font: bold {new_font_size * 1.2}px;")
        self.subtitel_label.setFixedHeight(cell_size*3)
        self.subtitel_label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter) 
        self.cni_logo_widget.setFixedSize(cell_size*4,cell_size*4)
        # Resize Seperator Line 1
        self.separator_label_1.setFixedHeight(int(cell_size/10))
        # Resize Direct Angle Input Elements
        self.direct_input_label.setStyleSheet(f"font: bold {new_font_size}px;")
        self.direct_input_label.setFixedHeight(cell_size*2)
        self.direct_input_label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        for k in range(16):
            self.direct_input_module_labels[k].setStyleSheet(f"font: bold {new_font_size}px;")
            self.direct_input_module_labels[k].setFixedHeight(new_font_size)
            self.direct_input_module_phi_label[k].setStyleSheet(f"color: #949494; font-size: {int(new_font_size/1.25)}px;")
            self.direct_input_module_theta_label[k].setStyleSheet(f"color: #949494; font-size: {int(new_font_size/1.25)}px;")
            self.direct_input_module_azimuth_value_box[k].setStyleSheet(f"padding-top: {int(0.1*3*grid_cell_height)}px; padding-bottom: {int(0.1*3*grid_cell_height)}px; padding-left: 0px; padding-right: -6px; margin: 0px; color: #FFFFFF; font-size: {int(new_font_size/1.25)}px;")
            self.direct_input_module_azimuth_value_box[k].setFixedHeight(3*grid_cell_height-int(0.2*3*grid_cell_height))
            self.direct_input_module_azimuth_value_box[k].setFixedWidth(6*grid_cell_width-int(0.1*6*grid_cell_width))
            self.direct_input_module_elevation_value_box[k].setStyleSheet(f"padding-top: {int(0.1*3*grid_cell_height)}px; padding-bottom: {int(0.1*3*grid_cell_height)}px; padding-left: 0px; padding-right: -6px; margin: 0px; color: #FFFFFF; font-size: {int(new_font_size/1.25)}px;")
            self.direct_input_module_elevation_value_box[k].setFixedHeight(3*grid_cell_height-int(0.2*3*grid_cell_height))
            self.direct_input_module_elevation_value_box[k].setFixedWidth(6*grid_cell_width-int(0.1*6*grid_cell_width))
            self.direct_input_module_checkbox[k].setStyleSheet(f"""QCheckBox {{margin: 0; padding: 0; width: {2*grid_cell_width-int(0.5*grid_cell_width)}px; height: {2*grid_cell_height-int(0.5*grid_cell_height)}px; }} QCheckBox::indicator {{width: {2*grid_cell_width-int(0.5*grid_cell_width)}px; height: {2*grid_cell_height-int(0.5*grid_cell_height)}px; }} """)
        self.direct_input_button_select_all.setStyleSheet(f"font: {int(new_font_size/1.25)}px; border: {int(new_font_size/10)}px solid #8bc34a; ")
        self.direct_input_button_select_all.setFixedSize(grid_cell_width*12-int(0.025*grid_cell_width*12),grid_cell_height*3-int(0.25*grid_cell_height*2)) 
        self.direct_input_button_unselect_all.setStyleSheet(f"font: {int(new_font_size/1.25)}px; border: {int(new_font_size/10)}px solid #8bc34a; ")
        self.direct_input_button_unselect_all.setFixedSize(grid_cell_width*12-int(0.025*grid_cell_width*12),grid_cell_height*3-int(0.25*grid_cell_height*2)) 
        self.set_configuration_button.setStyleSheet(f"font: {int(new_font_size/1.25)}px; border: {int(new_font_size/10)}px solid #8bc34a; ")
        self.set_configuration_button.setFixedSize(grid_cell_width*12-int(0.025*grid_cell_width*12),grid_cell_height*5-int(0.25*grid_cell_height*5)) 
        self.save_configuration_button.setStyleSheet(f"font: {int(new_font_size/1.25)}px; border: {int(new_font_size/10)}px solid #8bc34a; ")
        self.save_configuration_button.setFixedSize(grid_cell_width*12-int(0.025*grid_cell_width*12),grid_cell_height*5-int(0.25*grid_cell_height*5)) 
        # Resize Seperator Line 2
        self.separator_label_2.setFixedHeight(int(cell_size/10))
        # Resize IRS Beam Codebook
        self.beambook_label.setStyleSheet(f"font: bold {new_font_size}px;")
        self.beambook_label.setFixedHeight(cell_size*2)
        self.beambook_label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        items = self.beambook_widget.findChildren(QPushButton)
        for item in items:
            item.setStyleSheet(f"font: {int(new_font_size/1.25)}px; border: {int(new_font_size/10)}px solid #8bc34a; ")
            item.setFixedSize(grid_cell_width*18-int(0.025*grid_cell_width*2),grid_cell_height*3-int(0.25*grid_cell_height*2))   
        # Resize Switching Orchestration
        self.switching_orchestration_label.setStyleSheet(f"font: bold {new_font_size}px;")
        self.switching_orchestration_label.setFixedHeight(cell_size*2)
        self.switching_orchestration_label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.start_orchestration_btn.setStyleSheet(f"font: {int(new_font_size/1.25)}px; border: {int(new_font_size/10)}px solid #8bc34a; ")
        self.start_orchestration_btn.setFixedSize(grid_cell_width*12-int(0.025*grid_cell_width*12),grid_cell_height*3-int(0.25*grid_cell_height*2)) 
        self.reset_orchestration_btn.setStyleSheet(f"font: {int(new_font_size/1.25)}px; border: {int(new_font_size/10)}px solid #8bc34a; ")
        self.reset_orchestration_btn.setFixedSize(grid_cell_width*12-int(0.025*grid_cell_width*12),grid_cell_height*3-int(0.25*grid_cell_height*2)) 
        items = self.orchestration_widget.findChildren(Orchestration_item_widget)   
        for item in items:
            if item.orchestration_active:
                item.item.setStyleSheet(f"font: {int(min(self.width()//50, self.height()//50)/1.25)}px; border: {int(min(self.width()//50, self.height()//50)/10)}px solid #8bc34a; background-color: #639A00")
            else:
                item.item.setStyleSheet(f"font: {int(new_font_size/1.25)}px; border: {int(new_font_size/10)}px solid #8bc34a; ")
            item.item.setFixedSize(grid_cell_width*18-int(0.025*grid_cell_width*2),grid_cell_height*3-int(0.25*grid_cell_height*2))   
        items = self.orchestration_widget.findChildren(QDoubleSpinBox)
        for item in items:
            item.setStyleSheet(f"padding-top: {int(0.1*3*grid_cell_height)}px; padding-bottom: {int(0.1*3*grid_cell_height)}px; padding-left: 0px; padding-right: -6px; margin: 0px; color: #FFFFFF; font-size: {int(new_font_size/1.25)}px;")
            item.setFixedHeight(3*grid_cell_height-int(0.2*3*grid_cell_height))
            item.setFixedWidth(5*grid_cell_width-int(0.1*5*grid_cell_width))  
        # Resize Seperator Line 3
        self.separator_label_3.setFixedHeight(int(cell_size/10))
        # Resize Geometry Configuration Calculation
        self.geometry_label.setStyleSheet(f"font: bold {new_font_size}px;")
        self.geometry_label.setFixedHeight(cell_size*2)
        self.geometry_label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        for k in range(6):
            self.geometry_input[k].setStyleSheet(f"padding-top: {int(0.1*3*grid_cell_height)}px; padding-bottom: {int(0.1*3*grid_cell_height)}px; padding-left: 0px; padding-right: -6px; margin: 0px; color: #FFFFFF; font-size: {int(new_font_size/1.25)}px;")
            self.geometry_input[k].setFixedHeight(3*grid_cell_height-int(0.2*3*grid_cell_height))
            self.geometry_input[k].setFixedWidth(6*grid_cell_width-int(0.1*6*grid_cell_width))
        for k in range(2):
            self.intermodule_spacing_input[k].setStyleSheet(f"padding-top: {int(0.1*3*grid_cell_height)}px; padding-bottom: {int(0.1*3*grid_cell_height)}px; padding-left: 0px; padding-right: -6px; margin: 0px; color: #FFFFFF; font-size: {int(new_font_size/1.25)}px;")
            self.intermodule_spacing_input[k].setFixedHeight(3*grid_cell_height-int(0.2*3*grid_cell_height))
            self.intermodule_spacing_input[k].setFixedWidth(6*grid_cell_width-int(0.1*6*grid_cell_width))
        self.bs_label.setStyleSheet(f"font: bold {new_font_size//1.25}px;")
        self.bs_label.setFixedHeight(new_font_size)
        self.bs_label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.ue_label.setStyleSheet(f"font: bold {new_font_size//1.25}px;")
        self.ue_label.setFixedHeight(new_font_size)
        self.ue_label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        for k in range(6):
            self.coordinate_labels[k].setStyleSheet(f"color: #949494; font-size: {int(new_font_size/1.25)}px; padding-left: 1px")
        self.delta_y_label.setStyleSheet(f"color: #949494; font-size: {int(new_font_size/1.25)}px; padding-left: 1px")
        self.delta_z_label.setStyleSheet(f"color: #949494; font-size: {int(new_font_size/1.25)}px; padding-left: 1px")
        self.calculate_configuration_btn.setStyleSheet(f"font: {int(new_font_size/1.5)}px; border: {int(new_font_size/10)}px solid #8bc34a; ")
        self.calculate_configuration_btn.setFixedSize(grid_cell_width*12-int(0.025*grid_cell_width*12),grid_cell_height*4-int(0.25*grid_cell_height*3)) 
        self.intermodule_spacing_label.setStyleSheet(f"font: bold {new_font_size//1.25}px;")
        self.intermodule_spacing_label.setFixedHeight(new_font_size)
        self.individually_config_checkbox.setStyleSheet(f""" QCheckBox {{ margin: 0; padding: 0; width: {2*grid_cell_width-int(0.5*grid_cell_width)}px; height: {2*grid_cell_height-int(0.5*grid_cell_height)}px;}} QCheckBox::indicator {{ width: {2*grid_cell_width-int(0.5*grid_cell_width)}px; height: {2*grid_cell_height-int(0.5*grid_cell_height)}px; }} """)
        self.equally_config_checkbox.setStyleSheet(f""" QCheckBox {{ margin: 0; padding: 0; width: {2*grid_cell_width-int(0.5*grid_cell_width)}px; height: {2*grid_cell_height-int(0.5*grid_cell_height)}px; }} QCheckBox::indicator {{ width: {2*grid_cell_width-int(0.5*grid_cell_width)}px; height: {2*grid_cell_height-int(0.5*grid_cell_height)}px; }} """)
        self.individually_config_label.setStyleSheet(f"font: {new_font_size//1.25}px;")
        self.individually_config_label.setFixedHeight(new_font_size)
        self.individually_config_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.equally_config_label.setStyleSheet(f"font: {new_font_size//1.25}px;")
        self.equally_config_label.setFixedHeight(new_font_size)
        self.equally_config_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

    # Method to Handle Window Closing
    def closeEvent(self, event):
        if isinstance(self.orchestration_worker, Orchestration_timer):
            self.orchestration_worker.reset = True
        self.threadpool.waitForDone()
        while self.threadpool.activeThreadCount() > 0:
            time.sleep(0.1)
        event.accept()

    
# Main    
app = QApplication(sys.argv)
main_window = MainWindow()
apply_stylesheet(app, theme='dark_lightgreen.xml')
main_window.show()

app.exec()
