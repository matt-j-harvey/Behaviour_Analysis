import numpy as np
import pyqtgraph

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import os

import tables
import sys

sys.path.append("/home/matthew/Documents/Github_Code/Widefield_Preprocessing")

import Widefield_General_Functions





class lick_threshold_window(QWidget):

    def __init__(self, session_directory_list, parent=None):
        super(lick_threshold_window, self).__init__(parent)

        # Setup Window
        self.setWindowTitle("Set Lick Thresholds")
        self.setGeometry(0, 0, 1500, 500)

        # Create Variable Holders
        self.session_directory_list = session_directory_list
        self.channel_dictionary = Widefield_General_Functions.create_stimuli_dictionary()
        self.lick_threshold = 0.3
        self.current_session_index = 0
        self.lick_trace = None

        # Create Widgets

        # Current Session Label
        self.session_label = QLabel("Session: " + str(session_directory_list[self.current_session_index]))

        # Lick Threshold Display Widget
        self.lick_display_view_widget = QWidget()
        self.lick_display_view_widget_layout = QGridLayout()
        self.lick_display_view = pyqtgraph.PlotWidget()
        self.lick_display_view_widget_layout.addWidget(self.lick_display_view, 0, 0)
        self.lick_display_view_widget.setLayout(self.lick_display_view_widget_layout)
        self.lick_display_view_widget.setMinimumWidth(1000)

        # Session List Widget
        self.session_list_widget = QListWidget()
        for session in self.session_directory_list:
            session_name = session.split('/')[-1]
            self.session_list_widget.addItem(session_name)
        self.session_list_widget.setCurrentRow(0)
        self.session_list_widget.setFixedWidth(250)

        # Lick Threshold Spinner
        self.lick_threshold_spinner = QDoubleSpinBox()
        self.lick_threshold_spinner.setValue(self.lick_threshold)
        self.lick_threshold_spinner.setMinimum(0)
        self.lick_threshold_spinner.setMaximum(5)
        self.lick_threshold_spinner.valueChanged.connect(self.change_lick_threshold)
        self.lick_threshold_spinner.setSingleStep(0.01)

        # Set Lick Threshold Button
        self.set_lick_threshold_button = QPushButton("Set Lick Threshold")
        self.set_lick_threshold_button.clicked.connect(self.set_lick_threshold)

        # Create Layout
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        # Add Transformation Widgets
        self.layout.addWidget(self.session_label,                   0, 0, 1, 3)

        self.layout.addWidget(self.lick_display_view_widget,        1, 0, 1, 2)
        self.layout.addWidget(self.set_lick_threshold_button,       2, 0, 1, 1)
        self.layout.addWidget(self.lick_threshold_spinner,          2, 1, 1, 1)

        self.layout.addWidget(self.session_list_widget,             1, 2, 2, 1)


        # Plot First Item
        self.lick_threshold_line = pyqtgraph.InfiniteLine()
        self.lick_threshold_line.setAngle(0)
        self.lick_threshold_line.setValue(self.lick_threshold)
        self.lick_trace_curve = pyqtgraph.PlotCurveItem()
        self.lick_display_view.addItem(self.lick_threshold_line)
        self.lick_display_view.addItem(self.lick_trace_curve)
        self.load_session()


        self.show()

    def change_lick_threshold(self):

        self.lick_threshold = self.lick_threshold_spinner.value()

        # Plot Lick Trace
        #self.lick_display_view.plot(self.lick_trace)

        # Crate Horiztonal Line
        #horizontal_line = np.ones(len(self.lick_trace)) * self.lick_threshold
        #self.lick_display_view.plot(horizontal_line)
        self.lick_threshold_line.setValue(self.lick_threshold)



    def set_lick_threshold(self):

         # Get Output Path
        file_save_directory = os.path.join(self.session_directory_list[self.current_session_index], "Lick_Threshold.npy")

        # Save File
        np.save(file_save_directory, self.lick_threshold)

        # Increment Session Number
        self.current_session_index += 1

        # Close GUI if we have finished all the sessions
        if self.current_session_index == len(self.session_directory_list):
            self.close()

        # Else Load Next Session
        else:
            self.load_session()


    def load_session(self):

        # Load AI Data
        current_session = self.session_directory_list[self.current_session_index]
        ai_file_name = Widefield_General_Functions.get_ai_filename(current_session)
        ai_data = Widefield_General_Functions.load_ai_recorder_file(current_session + ai_file_name)

        # Get Lick Trace
        self.lick_trace = ai_data[self.channel_dictionary["Lick"]]

        # Plot Lick Trace
        self.lick_trace_curve.setData(self.lick_trace)

        # Update List Widget
        self.session_list_widget.setCurrentRow(self.current_session_index)


def set_lick_thresholds(session_directory):

    app = QApplication(sys.argv)

    window = lick_threshold_window(session_directory)
    window.show()

    app.exec_()


def create_session_list(base_directory):

    sub_directories = os.listdir(base_directory)

    session_list = []

    for directory in sub_directories:
        if "Switching" in directory or "Transition" in directory:
            session_list.append(os.path.join(base_directory,directory))

    return session_list


session_list = [
    "/media/matthew/Expansion/Widefield_Analysis/NXAK7.1B/2021_02_01_Discrimination_Imaging",
    "/media/matthew/Expansion/Widefield_Analysis/NXAK7.1B/2021_02_03_Discrimination_Imaging",
    "/media/matthew/Expansion/Widefield_Analysis/NXAK7.1B/2021_02_05_Discrimination_Imaging",
    "/media/matthew/Expansion/Widefield_Analysis/NXAK7.1B/2021_02_07_Discrimination_Imaging",
    "/media/matthew/Expansion/Widefield_Analysis/NXAK7.1B/2021_02_09_Discrimination_Imaging",
    "/media/matthew/Expansion/Widefield_Analysis/NXAK7.1B/2021_02_11_Discrimination_Imaging",
    "/media/matthew/Expansion/Widefield_Analysis/NXAK7.1B/2021_02_13_Discrimination_Imaging",
    "/media/matthew/Expansion/Widefield_Analysis/NXAK7.1B/2021_02_15_Discrimination_Imaging",
    "/media/matthew/Expansion/Widefield_Analysis/NXAK7.1B/2021_02_17_Discrimination_Imaging",
    "/media/matthew/Expansion/Widefield_Analysis/NXAK7.1B/2021_02_19_Discrimination_Imaging",
    "/media/matthew/Expansion/Widefield_Analysis/NXAK7.1B/2021_02_22_Discrimination_Imaging",
    "/media/matthew/Expansion/Widefield_Analysis/NXAK7.1B/2021_02_24_Discrimination_Imaging",

    "/media/matthew/Expansion/Widefield_Analysis/NXAK4.1B/2021_02_04_Discrimination_Imaging",
    "/media/matthew/Expansion/Widefield_Analysis/NXAK4.1B/2021_02_06_Discrimination_Imaging",
    "/media/matthew/Expansion/Widefield_Analysis/NXAK4.1B/2021_02_08_Discrimination_Imaging",
    "/media/matthew/Expansion/Widefield_Analysis/NXAK4.1B/2021_02_10_Discrimination_Imaging",
    "/media/matthew/Expansion/Widefield_Analysis/NXAK4.1B/2021_02_12_Discrimination_Imaging",
    "/media/matthew/Expansion/Widefield_Analysis/NXAK4.1B/2021_02_14_Discrimination_Imaging",
    "/media/matthew/Expansion/Widefield_Analysis/NXAK4.1B/2021_02_22_Discrimination_Imaging",

    "/media/matthew/Expansion/Widefield_Analysis/NXAK14.1A/2021_04_29_Discrimination_Imaging",
    "/media/matthew/Expansion/Widefield_Analysis/NXAK14.1A/2021_05_01_Discrimination_Imaging",
    "/media/matthew/Expansion/Widefield_Analysis/NXAK14.1A/2021_05_03_Discrimination_Imaging",
    "/media/matthew/Expansion/Widefield_Analysis/NXAK14.1A/2021_05_05_Discrimination_Imaging",
    "/media/matthew/Expansion/Widefield_Analysis/NXAK14.1A/2021_05_07_Discrimination_Imaging",
    "/media/matthew/Expansion/Widefield_Analysis/NXAK14.1A/2021_05_09_Discrimination_Imaging",

    "/media/matthew/Seagate Expansion Drive1/Processed_Widefield_Data/NXAK22.1A/2021_09_25_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive1/Processed_Widefield_Data/NXAK22.1A/2021_09_29_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive1/Processed_Widefield_Data/NXAK22.1A//2021_10_01_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive1/Processed_Widefield_Data/NXAK22.1A/2021_10_03_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive1/Processed_Widefield_Data/NXAK22.1A/2021_10_05_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive1/Processed_Widefield_Data/NXAK22.1A/2021_10_07_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive1/Processed_Widefield_Data/NXAK22.1A/2021_10_08_Discrimination_Imaging",

    "/media/matthew/Seagate Expansion Drive1/Processed_Widefield_Data/NRXN78.1D/2020_11_15_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive1/Processed_Widefield_Data/NRXN78.1D/2020_11_16_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive1/Processed_Widefield_Data/NRXN78.1D/2020_11_17_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive1/Processed_Widefield_Data/NRXN78.1D/2020_11_19_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive1/Processed_Widefield_Data/NRXN78.1D/2020_11_23_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive1/Processed_Widefield_Data/NRXN78.1D/2020_11_25_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive1/Processed_Widefield_Data/NRXN78.1D/2020_11_14_Discrimination_Imaging",

    "/media/matthew/Seagate Expansion Drive1/Processed_Widefield_Data/NRXN78.1A/2020_11_15_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive1/Processed_Widefield_Data/NRXN78.1A/2020_11_16_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive1/Processed_Widefield_Data/NRXN78.1A/2020_11_17_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive1/Processed_Widefield_Data/NRXN78.1A/2020_11_19_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive1/Processed_Widefield_Data/NRXN78.1A/2020_11_21_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive1/Processed_Widefield_Data/NRXN78.1A/2020_11_24_Discrimination_Imaging",
]




session_list = [

    # Mutants
    # 72.1A - Slow Learner
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NRXN71.2A/2020_11_13_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NRXN71.2A/2020_11_14_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NRXN71.2A/2020_11_15_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NRXN71.2A/2020_11_16_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NRXN71.2A/2020_11_17_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NRXN71.2A/2020_11_18_Discrimination_Behaviour",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NRXN71.2A/2020_11_19_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NRXN71.2A/2020_11_20_Discrimination_Behaviour",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NRXN71.2A/2020_11_21_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NRXN71.2A/2020_11_22_Discrimination_Behaviour",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NRXN71.2A/2020_11_23_Discrimination_Behaviour",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NRXN71.2A/2020_11_24_Discrimination_Behaviour",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NRXN71.2A/2020_11_25_Discrimination_Behaviour",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NRXN71.2A/2020_11_26_Discrimination_Behaviour",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NRXN71.2A/2020_11_27_Discrimination_Behaviour",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NRXN71.2A/2020_11_28_Discrimination_Behaviour",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NRXN71.2A/2020_11_29_Discrimination_Behaviour",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NRXN71.2A/2020_11_30_Discrimination_Behaviour",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NRXN71.2A/2020_12_01_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NRXN71.2A/2020_12_02_Discrimination_Behaviour",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NRXN71.2A/2020_12_03_Discrimination_Imaging",

    # 4.1A Slow Learner
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK4.1A/2021_02_02_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK4.1A/2021_02_03_Discrimination_Behaviour",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK4.1A/2021_02_04_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK4.1A/2021_02_05_Discrimination_Behaviour",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK4.1A/2021_02_06_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK4.1A/2021_02_07_Discrimination_Behaviour",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK4.1A/2021_02_08_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK4.1A/2021_02_09_Discrimination_Behaviour",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK4.1A/2021_02_10_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK4.1A/2021_02_11_Discrimination_Behaviour",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK4.1A/2021_02_12_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK4.1A/2021_02_13_Discrimination_Behaviour",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK4.1A/2021_02_14_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK4.1A/2021_02_15_Discrimination_Behaviour",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK4.1A/2021_02_16_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK4.1A/2021_02_17_Discrimination_Behaviour",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK4.1A/2021_02_18_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK4.1A/2021_02_19_Discrimination_Behaviour",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK4.1A/2021_02_20_Discrimination_Behaviour",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK4.1A/2021_02_21_Discrimination_Behaviour",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK4.1A/2021_02_22_Discrimination_Behaviour",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK4.1A/2021_02_23_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK4.1A/2021_02_24_Discrimination_Behaviour",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK4.1A/2021_02_25_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK4.1A/2021_02_26_Discrimination_Behaviour",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK4.1A/2021_02_27_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK4.1A/2021_02_28_Discrimination_Behaviour",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK4.1A/2021_03_01_Discrimination_Imaging",

    # 10.1A Fast learner
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK10.1A/2021_04_30_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK10.1A/2021_05_01_Discrimination_Behaviour",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK10.1A/2021_05_02_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK10.1A/2021_05_04_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK10.1A/2021_05_05_Discrimination_Behaviour",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK10.1A/2021_05_06_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK10.1A/2021_05_07_Discrimination_Behaviour",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK10.1A/2021_05_08_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK10.1A/2021_05_09_Discrimination_Behaviour",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK10.1A/2021_05_10_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK10.1A/2021_05_11_Discrimination_Behaviour",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK10.1A/2021_05_12_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK10.1A/2021_05_13_Discrimination_Behaviour",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK10.1A/2021_05_14_Discrimination_Imaging",

    # 16.1B Slow Learner
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK16.1B/2021_04_30_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK16.1B/2021_05_01_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK16.1B/2021_05_02_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK16.1B/2021_05_03_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK16.1B/2021_05_04_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK16.1B/2021_05_05_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK16.1B/2021_05_06_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK16.1B/2021_05_07_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK16.1B/2021_05_08_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK16.1B/2021_05_09_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK16.1B/2021_05_10_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK16.1B/2021_05_11_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK16.1B/2021_05_12_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK16.1B/2021_05_13_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK16.1B/2021_05_14_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK16.1B/2021_05_16_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK16.1B/2021_05_17_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK16.1B/2021_05_18_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK16.1B/2021_05_19_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK16.1B/2021_05_20_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK16.1B/2021_05_21_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK16.1B/2021_05_22_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK16.1B/2021_05_23_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK16.1B/2021_05_24_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK16.1B/2021_05_25_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK16.1B/2021_05_26_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK16.1B/2021_05_27_Discrimination_Behaviour",

    # 24.1C Fast Learner
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK24.1C/2021_09_20_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK24.1C/2021_09_21_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK24.1C/2021_09_22_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK24.1C/2021_09_23_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK24.1C/2021_09_24_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK24.1C/2021_09_25_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK24.1C/2021_09_26_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK24.1C/2021_09_27_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK24.1C/2021_09_28_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK24.1C/2021_09_29_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK24.1C/2021_09_30_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK24.1C/2021_10_01_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK24.1C/2021_10_02_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK24.1C/2021_10_03_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK24.1C/2021_10_04_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK24.1C/2021_10_05_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK24.1C/2021_10_06_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK24.1C/2021_10_08_Discrimination_Imaging",

    # 20.1B Slow Leaner
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK20.1B/2021_09_28_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK20.1B/2021_09_29_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK20.1B/2021_09_30_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK20.1B/2021_10_01_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK20.1B/2021_10_02_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK20.1B/2021_10_03_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK20.1B/2021_10_04_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK20.1B/2021_10_05_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK20.1B/2021_10_06_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK20.1B/2021_10_07_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK20.1B/2021_10_08_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK20.1B/2021_10_09_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK20.1B/2021_10_10_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK20.1B/2021_10_11_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK20.1B/2021_10_12_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK20.1B/2021_10_13_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK20.1B/2021_10_14_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK20.1B/2021_10_15_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK20.1B/2021_10_16_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK20.1B/2021_10_17_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK20.1B/2021_10_18_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK20.1B/2021_10_19_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK20.1B/2021_10_20_Discrimination_Behaviour",

    # Control Mice
    # 78.1A - Fast Learner
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NRXN78.1A/2020_11_14_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NRXN78.1A/2020_11_15_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NRXN78.1A/2020_11_16_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NRXN78.1A/2020_11_17_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NRXN78.1A/2020_11_18_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NRXN78.1A/2020_11_19_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NRXN78.1A/2020_11_20_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NRXN78.1A/2020_11_21_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NRXN78.1A/2020_11_22_Discrimination_Behaviour",

    # 78.1D - Fast learner
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NRXN78.1D/2020_11_14_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NRXN78.1D/2020_11_15_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NRXN78.1D/2020_11_16_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NRXN78.1D/2020_11_17_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NRXN78.1D/2020_11_18_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NRXN78.1D/2020_11_19_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NRXN78.1D/2020_11_20_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NRXN78.1D/2020_11_21_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NRXN78.1D/2020_11_22_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NRXN78.1D/2020_11_23_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NRXN78.1D/2020_11_24_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NRXN78.1D/2020_11_25_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NRXN78.1D/2020_11_26_Discrimination_Behaviour",

    # 4.1B
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK4.1B/2021_02_04_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK4.1B/2021_02_05_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK4.1B/2021_02_06_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK4.1B/2021_02_07_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK4.1B/2021_02_08_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK4.1B/2021_02_09_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK4.1B/2021_02_10_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK4.1B/2021_02_11_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK4.1B/2021_02_12_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK4.1B/2021_02_13_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK4.1B/2021_02_14_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK4.1B/2021_02_15_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK4.1B/2021_02_18_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK4.1B/2021_02_19_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK4.1B/2021_02_20_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK4.1B/2021_02_21_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK4.1B/2021_02_22_Discrimination_Imaging",

    # 14.1A FSt learner
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK14.1A/2021_04_29_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK14.1A/2021_04_30_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK14.1A/2021_05_01_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK14.1A/2021_05_02_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK14.1A/2021_05_03_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK14.1A/2021_05_04_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK14.1A/2021_05_05_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK14.1A/2021_05_06_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK14.1A/2021_05_07_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK14.1A/2021_05_08_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK14.1A/2021_05_09_Discrimination_Imaging",

    # 22.1A
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK22.1A/2021_09_25_Discrimination_Imaging",
    #"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK22.1A/2021_09_26_Discrimination_Behaviour",
    ]



session_list = [
                "/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NXAK16.1B/2021_05_22_Discrimination_Imaging",
                "/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NXAK16.1B/2021_05_24_Discrimination_Imaging",
                "/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NXAK16.1B/2021_05_26_Discrimination_Imaging",
                "/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NXAK16.1B/2021_06_04_Discrimination_Imaging",
                "/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NXAK16.1B/2021_06_15_Discrimination_Imaging"]

session_list = [
    # 24.1C - 10
    r"/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NXAK24.1C/2021_09_20_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NXAK24.1C/2021_09_22_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NXAK24.1C/2021_09_24_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NXAK24.1C/2021_09_26_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NXAK24.1C/2021_09_28_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NXAK24.1C/2021_09_30_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NXAK24.1C/2021_10_02_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NXAK24.1C/2021_10_04_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NXAK24.1C/2021_10_06_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NXAK24.1C/2021_10_08_Discrimination_Imaging",

]

session_list = [
    # 10.1A - 8
    r"/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NXAK10.1A/2021_04_30_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NXAK10.1A/2021_05_02_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NXAK10.1A/2021_05_04_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NXAK10.1A/2021_05_06_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NXAK10.1A/2021_05_08_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NXAK10.1A/2021_05_10_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NXAK10.1A/2021_05_12_Discrimination_Imaging",
    ]

session_list = [
    "/media/matthew/Expansion/Widefield_Analysis/NXAK14.1A/2021_06_13_Transition_Imaging",  # not yet uploaded
    "/media/matthew/Expansion/Widefield_Analysis/NXAK14.1A/2021_06_15_Transition_Imaging",  # not yet uploaded
    "/media/matthew/Expansion/Widefield_Analysis/NXAK14.1A/2021_06_17_Transition_Imaging",  # motion corrected matches
]

session_list = [
    "/media/matthew/Expansion/Widefield_Analysis/NXAK22.1A/2021_10_29_Transition_Imaging",
    "/media/matthew/Expansion/Widefield_Analysis/NXAK22.1A/2021_11_03_Transition_Imaging",
    "/media/matthew/Expansion/Widefield_Analysis/NXAK22.1A/2021_11_05_Transition_Imaging",
]

session_list = [r"/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NRXN78.1D/2020_12_05_Switching_Imaging"]


session_list = [
    "/media/matthew/Expansion/Widefield_Analysis/NXAK16.1B/2021_07_08_Transition_Imaging",
    "/media/matthew/Expansion/Widefield_Analysis/NXAK4.1A/2021_04_12_Transition_Imaging",
    "/media/matthew/Expansion/Widefield_Analysis/NXAK20.1B/2021_11_22_Transition_Imaging",
    "/media/matthew/Expansion/Widefield_Analysis/NXAK24.1C/2021_11_10_Transition_Imaging",
    ]


session_list = [
    r"/media/matthew/Seagate Expansion Drive/Widefield_Imaging/Processed_Widefield_Data/NRXN71.2A/2020_11_13_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive/Widefield_Imaging/Processed_Widefield_Data/NRXN71.2A/2020_11_14_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive/Widefield_Imaging/Processed_Widefield_Data/NRXN71.2A/2020_11_15_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive/Widefield_Imaging/Processed_Widefield_Data/NRXN71.2A/2020_11_16_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive/Widefield_Imaging/Processed_Widefield_Data/NRXN71.2A/2020_11_17_Discrimination_Imaging",

    r"/media/matthew/Seagate Expansion Drive/Widefield_Imaging/Processed_Widefield_Data/NRXN71.2A/2020_11_19_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive/Widefield_Imaging/Processed_Widefield_Data/NRXN71.2A/2020_11_21_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive/Widefield_Imaging/Processed_Widefield_Data/NRXN71.2A/2020_11_23_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive/Widefield_Imaging/Processed_Widefield_Data/NRXN71.2A/2020_11_25_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive/Widefield_Imaging/Processed_Widefield_Data/NRXN71.2A/2020_11_27_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive/Widefield_Imaging/Processed_Widefield_Data/NRXN71.2A/2020_11_29_Discrimination_Imaging",

    r"/media/matthew/Seagate Expansion Drive/Widefield_Imaging/Processed_Widefield_Data/NRXN71.2A/2020_12_01_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive/Widefield_Imaging/Processed_Widefield_Data/NRXN71.2A/2020_12_03_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive/Widefield_Imaging/Processed_Widefield_Data/NRXN71.2A/2020_12_05_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive/Widefield_Imaging/Processed_Widefield_Data/NRXN71.2A/2020_12_07_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive/Widefield_Imaging/Processed_Widefield_Data/NRXN71.2A/2020_12_09_Discrimination_Imaging",
]

session_list = ["/media/matthew/External_Harddrive_1/Processed_Widefield_Data/Beverly/2022_05_16_Mirror_Imaging",
                "/media/matthew/External_Harddrive_1/Processed_Widefield_Data/Beverly/2022_05_18_Mirror_Imaging",
                "/media/matthew/External_Harddrive_1/Processed_Widefield_Data/Beverly/2022_05_23_mirror_imaging",
                "/media/matthew/External_Harddrive_1/Processed_Widefield_Data/Beverly/2022_05_27_mirror_imaging"]

session_list = ["/media/matthew/External_Harddrive_1/Processed_Widefield_Data/NRXN78.1D/2020_12_07_Switching_Imaging"]


set_lick_thresholds(session_list)