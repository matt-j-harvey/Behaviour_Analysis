import math

import numpy as np
import matplotlib.pyplot as plt
import sys
import h5py
import os
import tables
from scipy import signal, ndimage, stats
from sklearn.neighbors import KernelDensity
import cv2
from matplotlib import gridspec, patches


sys.path.append("/home/matthew/Documents/Github_Code/Widefield_Preprocessing")

import Widefield_General_Functions
import Plot_Behaviour_Matrix


def get_ai_filename(base_directory):

    #Get List of all files
    file_list = os.listdir(base_directory)
    ai_filename = None

    #Get .h5 files
    h5_file_list = []
    for file in file_list:
        if file[-3:] == ".h5":
            h5_file_list.append(file)

    #File the H5 file which is two dates seperated by a dash
    for h5_file in h5_file_list:
        original_filename = h5_file

        #Remove Ending
        h5_file = h5_file[0:-3]

        #Split By Dashes
        h5_file = h5_file.split("-")

        if len(h5_file) == 2 and h5_file[0].isnumeric() and h5_file[1].isnumeric():
            ai_filename = "/" + original_filename
            return ai_filename




def load_ai_recorder_file(ai_recorder_file_location):
    table = tables.open_file(ai_recorder_file_location, mode='r')
    data = table.root.Data

    number_of_seconds = np.shape(data)[0]
    number_of_channels = np.shape(data)[1]
    sampling_rate = np.shape(data)[2]

    data_matrix = np.zeros((number_of_channels, number_of_seconds * sampling_rate))

    for second in range(number_of_seconds):
        data_window = data[second]
        start_point = second * sampling_rate

        for channel in range(number_of_channels):
            data_matrix[channel, start_point:start_point + sampling_rate] = data_window[channel]

    data_matrix = np.clip(data_matrix, a_min=0, a_max=None)
    return data_matrix


def get_ai_filename(base_directory):

    #Get List of all files
    file_list = os.listdir(base_directory)
    ai_filename = None

    #Get .h5 files
    h5_file_list = []
    for file in file_list:
        if file[-3:] == ".h5":
            h5_file_list.append(file)

    #File the H5 file which is two dates seperated by a dash
    for h5_file in h5_file_list:
        original_filename = h5_file

        #Remove Ending
        h5_file = h5_file[0:-3]

        #Split By Dashes
        h5_file = h5_file.split("-")

        if len(h5_file) == 2 and h5_file[0].isnumeric() and h5_file[1].isnumeric():
            ai_filename = "/" + original_filename
            print("Ai filename is: ", ai_filename)
            return ai_filename


def get_step_onsets(trace, threshold=1, window=10):
    state = 0
    number_of_timepoints = len(trace)
    onset_times = []
    time_below_threshold = 0

    onset_line = []

    for timepoint in range(number_of_timepoints):
        if state == 0:
            if trace[timepoint] > threshold:
                state = 1
                onset_times.append(timepoint)
                time_below_threshold = 0
            else:
                pass
        elif state == 1:
            if trace[timepoint] > threshold:
                time_below_threshold = 0
            else:
                time_below_threshold += 1
                if time_below_threshold > window:
                    state = 0
                    time_below_threshold = 0
        onset_line.append(state)

    return onset_times



def create_stimuli_dictionary():
    channel_index_dictionary = {
        "Photodiode": 0,
        "Reward": 1,
        "Lick": 2,
        "Visual 1": 3,
        "Visual 2": 4,
        "Odour 1": 5,
        "Odour 2": 6,
        "Irrelevance": 7,
        "Running": 8,
        "Trial End": 9,
        "Camera Trigger": 10,
        "Camera Frames": 11,
        "LED 1": 12,
        "LED 2": 13,
        "Mousecam": 14,
        "Optogenetics": 15,
    }
    return channel_index_dictionary


def get_offset(onset, stream, threshold=0.5):

    count = 0
    on = True
    while on:
        if onset + count < len(stream):
            if stream[onset + count] < threshold and count > 10:
                on = False
                return onset + count
            else:
                count += 1

        else:
            return np.nan




def get_frame_indexes(frame_stream):
    frame_indexes = {}
    state = 1
    threshold = 2
    count = 0

    for timepoint in range(0, len(frame_stream)):

        if frame_stream[timepoint] > threshold:
            if state == 0:
                state = 1
                frame_indexes[timepoint] = count
                count += 1

        else:
            if state == 1:
                state = 0
            else:
                pass

    return frame_indexes






def extract_onsets(base_directory, ai_filename, save_directory, lick_threshold=0.13, visualise_lick_threshold=True):

    # Load AI Data
    ai_data = load_ai_recorder_file(base_directory + ai_filename)

    # Create Stimuli Dictionary
    stimuli_dictionary = create_stimuli_dictionary()

    # Load Traces
    lick_trace = ai_data[stimuli_dictionary["Lick"]]
    running_trace = ai_data[stimuli_dictionary["Running"]]
    vis_1_trace = ai_data[stimuli_dictionary["Visual 1"]]
    vis_2_trace = ai_data[stimuli_dictionary["Visual 2"]]
    reward_trace = ai_data[stimuli_dictionary["Reward"]]
    frame_trace = ai_data[stimuli_dictionary["LED 1"]]
    end_trace = ai_data[stimuli_dictionary["Trial End"]]
    mousecam_trace = ai_data[stimuli_dictionary["Mousecam"]]
    photodiode_trace = ai_data[stimuli_dictionary["Photodiode"]]

    if visualise_lick_threshold:
        plt.plot(lick_trace)
        plt.axhline(lick_threshold, c='k')
        split_directory = base_directory.split('/')
        session_name = split_directory[-2] + "_" + split_directory[-1]
        plt.title(session_name)
        plt.show()

    # Get Onsets
    vis_1_onsets    = get_step_onsets(vis_1_trace)
    vis_2_onsets    = get_step_onsets(vis_2_trace)
    lick_onsets     = get_step_onsets(lick_trace, threshold=lick_threshold, window=10)
    reward_onsets   = get_step_onsets(reward_trace)
    frame_onsets    = get_step_onsets(frame_trace)
    end_onsets      = get_step_onsets(end_trace)

    # Get Widefield Frame Indexes
    widefield_frame_onsets = get_frame_indexes(frame_trace)
    np.save(os.path.join(save_directory, "Frame_Times.npy"), widefield_frame_onsets)

    # Get Mousecam Frame Indexes
    mousecam_frame_onsets = get_frame_indexes(mousecam_trace)
    np.save(os.path.join(save_directory, "Mousecam_Frame_Times.npy"), mousecam_frame_onsets)


    onsets_dictionary ={"vis_1_onsets":vis_1_onsets,
                        "vis_2_onsets":vis_2_onsets,
                        "lick_onsets":lick_onsets,
                        "reward_onsets":reward_onsets,
                        "frame_onsets":frame_onsets,
                        "trial_ends":end_onsets}

    traces_dictionary ={"lick_trace":lick_trace,
                        "running_trace":running_trace,
                        "vis_1_trace":vis_1_trace,
                        "vis_2_trace":vis_2_trace,
                        "reward_trace":reward_trace,
                        "frame_trace":frame_trace,
                        "end_trace":end_trace,
                        "photodiode_trace":photodiode_trace}

    return onsets_dictionary, traces_dictionary



def get_trial_type(onset, onsets_dictionary):

    vis_1_onsets = onsets_dictionary["vis_1_onsets"]
    vis_2_onsets = onsets_dictionary["vis_2_onsets"]

    if onset in vis_1_onsets:
        return 1
    elif onset in vis_2_onsets:
        return 2



def get_trial_end(onset, onsets_dictionary, traces_dictionary):

    # If Not End - AI May Have Stopped Prematurely - Trial End Will Be Last Part of AI Recorder
    ends_trace = traces_dictionary['end_trace']

    trial_ends = onsets_dictionary["trial_ends"]
    trial_ends.sort()

    for end in trial_ends:
        if end > onset:
            return end
    return len(ends_trace)


def get_stimuli_offset(onset, trial_type, traces_dictionary):

    if trial_type == 1:
        stream = traces_dictionary['vis_1_trace']
    elif trial_type == 2:
        stream = traces_dictionary['vis_2_trace']

    offset = get_offset(onset, stream)
    return offset


def check_lick(onset, offset, traces_dictionary, lick_threshold):

    # Get Lick Trace
    lick_trace = traces_dictionary['lick_trace']

    # Get Lick Trace For Trial
    trial_lick_trace = lick_trace[onset:offset]

    if np.max(trial_lick_trace) >= lick_threshold:
        return 1
    else:
        return 0


def check_reward_outcome(onset, trial_end, traces_dictionary):

    reward_trace = traces_dictionary['reward_trace']

    trial_reward_trace = reward_trace[onset:trial_end]

    if np.max(trial_reward_trace > 0.5):
        return  1
    else:
        return 0




def check_correct(trial_type, lick):

    if trial_type == 1 or trial_type == 3:
        if lick == 1:
            return 1
        else:
            return 0

    elif trial_type == 2 or trial_type == 4:
        if lick == 0:
            return 1
        else:
            return 0




def classify_trial(onset, onsets_dictionary, traces_dictionary, trial_index, lick_threshold):

    """
    0 trial_index = int, index of trial
    1 trial_type = 1 - rewarded visual, 2 - unrewarded visual,
    2 lick = 1- lick, 0 - no lick
    3 correct = 1 - correct, 0 - incorrect
    4 rewarded = 1- yes, 0 - no
    5 preeceded_by_irrel = 0 - no, 1 - yes
    6 irrel_type = 1 - rewarded grating, 2 - unrearded grating
    7 ignore_irrel = 0 - licked to irrel, 1 - ignored irrel, nan - no irrel,
    8 block_number = int, index of block
    9 first_in_block = 1 - yes, 2- no
    10 in_block_of_stable_performance = 1 - yes, 2 - no
    11 onset = float onset of major stimuli
    12 stimuli_offset = float offset of major stimuli
    13 irrel_onset = float onset of any irrel stimuli, nan = no irrel stimuli
    14 irrel_offset = float offset of any irrel stimuli, nan = no irrel stimuli
    15 trial_end = float end of trial
    16 Photodiode Onset = Adjusted Visual stimuli onset to when the photodiode detects the stimulus
    17 Photodiode Offset = Adjusted Visual Stimuli Offset to when the photodiode detects the stimulus
    """

    # Get Trial Type
    trial_type = get_trial_type(onset, onsets_dictionary)

    # Get Trial End
    trial_end = get_trial_end(onset, onsets_dictionary, traces_dictionary)

    # Get Stimuli Offset
    stimuli_offset = get_stimuli_offset(onset, trial_type, traces_dictionary)

    # Get Mouse Response
    lick = check_lick(onset, trial_end, traces_dictionary, lick_threshold)

    # Check Correct
    correct = check_correct(trial_type, lick)

    # Check Reward Outcome
    rewarded = check_reward_outcome(onset, trial_end, traces_dictionary)


    # Get Irrel Details
    preeceded_by_irrel = None
    irrel_type = None
    irrel_onset = None
    irrel_offset = None
    ignore_irrel = None
    photodiode_onset = None
    photodiode_offset = None
    first_in_block = None
    in_block_of_stable_performance = None
    block_number = None


    trial_vector = [trial_index,
                    trial_type,
                    lick,
                    correct,
                    rewarded,
                    preeceded_by_irrel,
                    irrel_type,
                    ignore_irrel,
                    block_number,
                    first_in_block,
                    in_block_of_stable_performance,
                    onset,
                    stimuli_offset,
                    irrel_onset,
                    irrel_offset,
                    trial_end,
                    photodiode_onset,
                    photodiode_offset]

    return trial_vector



def print_behaviour_matrix(behaviour_matrix):

    for t in behaviour_matrix:
        print("Trial:" ,t[0]," Type:",t[1]," Lick:",t[2]," Correct:",t[3]," Rewarded:",t[4]," Irrel_Preceed:",t[5]," Irrel Type:",t[6]," Ignore Irrel:",t[7],"Block Number:",t[8],"First In Block:",t[9],"In Stable Window:",t[10],"Onset:",t[11]," Offset:",t[12]," Photodiode_Onset:",t[16]," Photodiode_Offset:",t[17])






def get_nearest_frame(stimuli_onsets, frame_times):

    #frame_times = frame_onsets.keys()
    nearest_frames = []
    window_size = 50

    if len(stimuli_onsets) > 0:

        print("Stimuli Onsets", stimuli_onsets)
        for onset in stimuli_onsets:
            smallest_distance = 1000
            closest_frame = None

            window_start = int(onset - window_size)
            window_stop  = int(onset + window_size)

            for timepoint in range(window_start, window_stop):

                #There is a frame at this time
                if timepoint in frame_times:
                    distance = abs(onset - timepoint)

                    if distance < smallest_distance:
                        smallest_distance = distance
                        closest_frame = frame_times.index(timepoint)
                        #closest_frame = frame_onsets[timepoint]

            if closest_frame != None:
                if closest_frame > 11:
                    nearest_frames.append(closest_frame)

        nearest_frames = np.array(nearest_frames)
    return nearest_frames



def get_times_from_behaviour_matrix(behaviour_matrix, selected_trials, onset_category):
    trial_times = []
    for trial in selected_trials:
        relevant_onset = behaviour_matrix[trial][onset_category]
        trial_times.append(relevant_onset)
    return trial_times




def save_onsets(behaviour_matrix, selected_trials, onsets_dictionary, save_directory):

    # Load Trials
    visual_1_all =          selected_trials[0]
    visual_2_all =          selected_trials[1]
    visual_1_correct =      selected_trials[2]
    visual_2_correct =      selected_trials[3]
    visual_1_incorrect =    selected_trials[4]
    visual_2_incorrect =    selected_trials[5]

    # Get Stimuli Times For Each Trial Cateogry
    visual_1_all_times          = get_times_from_behaviour_matrix(behaviour_matrix, visual_1_all, 11)
    visual_2_all_times          = get_times_from_behaviour_matrix(behaviour_matrix, visual_2_all, 11)
    visual_1_correct_times      = get_times_from_behaviour_matrix(behaviour_matrix, visual_1_correct, 11)
    visual_2_correct_times      = get_times_from_behaviour_matrix(behaviour_matrix, visual_2_correct, 11)
    visual_1_incorrect_times    = get_times_from_behaviour_matrix(behaviour_matrix, visual_1_incorrect, 11)
    visual_2_incorrect_times    = get_times_from_behaviour_matrix(behaviour_matrix, visual_2_incorrect, 11)

    # Load Frame Onsets
    frame_onsets = onsets_dictionary['frame_onsets']

    # Get Frames For Each Stimuli Category
    visual_1_all_onsets         = get_nearest_frame(visual_1_all_times, frame_onsets)
    visual_2_all_onsets         = get_nearest_frame(visual_2_all_times, frame_onsets)
    visual_1_correct_onsets     = get_nearest_frame(visual_1_correct_times, frame_onsets)
    visual_2_correct_onsets     = get_nearest_frame(visual_2_correct_times, frame_onsets)
    visual_1_incorrect_onsets   = get_nearest_frame(visual_1_incorrect_times, frame_onsets)
    visual_2_incorrect_onsets   = get_nearest_frame(visual_2_incorrect_times, frame_onsets)

    # Save Onsets
    np.save(os.path.join(save_directory, "visual_1_all_onsets.npy"), visual_1_all_onsets)
    np.save(os.path.join(save_directory, "visual_2_all_onsets.npy"), visual_2_all_onsets)
    np.save(os.path.join(save_directory, "visual_1_correct_onsets.npy"), visual_1_correct_onsets)
    np.save(os.path.join(save_directory, "visual_2_correct_onsets.npy"), visual_2_correct_onsets)
    np.save(os.path.join(save_directory, "visual_1_incorrect_onsets.npy"), visual_1_incorrect_onsets)
    np.save(os.path.join(save_directory, "visual_2_incorrect_onsets.npy"), visual_2_incorrect_onsets)



def get_selected_trials(behaviour_matrix):

    # Get Selected Trials
    visual_1_all = []
    visual_2_all = []
    visual_1_correct = []
    visual_2_correct = []
    visual_1_incorrect = []
    visual_2_incorrect = []

    # Iterate Through All Trials
    number_of_trials = np.shape(behaviour_matrix)[0]
    for trial_index in range(number_of_trials):
        trial_type = behaviour_matrix[trial_index][1]
        trial_is_correct = behaviour_matrix[trial_index][3]

        # Classify Rewarded Trials
        if trial_type == 1:
            visual_1_all.append(trial_index)

            if trial_is_correct == 1:
                visual_1_correct.append(trial_index)
            else:
                visual_1_incorrect.append(trial_index)

        # Classify Unrewarded Trials
        if trial_type == 2:
            visual_2_all.append(trial_index)

            if trial_is_correct == 1:
                visual_2_correct.append(trial_index)
            else:
                visual_2_incorrect.append(trial_index)

    selected_trials_list = [visual_1_all,
                            visual_2_all,
                            visual_1_correct,
                            visual_2_correct,
                            visual_1_incorrect,
                            visual_2_incorrect]

    return selected_trials_list




def create_behaviour_matrix(base_directory, behaviour_only=False):
    print("Creating Behaviour Matrix For Session: ", base_directory)

    # Get AI Filename
    ai_filename = get_ai_filename(base_directory)

    # Load Lick Threshold
    lick_threshold = np.load(os.path.join(base_directory, "Lick_Threshold.npy"))
    print("Lick Threshold : ", lick_threshold)

    # Create Save Directory
    save_directory = os.path.join(base_directory, "Stimuli_Onsets")
    if not os.path.exists(save_directory):
        os.mkdir(save_directory)

    # Get Trace and Onsets Dictionary
    onsets_dictionary, traces_dictionary = extract_onsets(base_directory, ai_filename, save_directory, lick_threshold=lick_threshold, visualise_lick_threshold=False)

    # Create Trial Onsets List
    vis_1_onsets = onsets_dictionary["vis_1_onsets"]
    vis_2_onsets = onsets_dictionary["vis_2_onsets"]
    trial_onsets = vis_1_onsets + vis_2_onsets
    trial_onsets.sort()

    # Classify Trials
    trial_matrix = []
    trial_index = 0
    for trial in trial_onsets:
        trial_vector = classify_trial(trial, onsets_dictionary, traces_dictionary, trial_index, lick_threshold=lick_threshold)
        trial_matrix.append(trial_vector)
        trial_index += 1
    trial_matrix = np.array(trial_matrix)

    # Get Selected Trials
    selected_trials = get_selected_trials(trial_matrix)

    # Print Behaviour Matrix
    print_behaviour_matrix(trial_matrix)

    # Save Trials
    if not behaviour_only:
        save_onsets(trial_matrix, selected_trials, onsets_dictionary, save_directory)

    # Plot Behaviour Matrix
    Plot_Behaviour_Matrix.plot_behaviour_maxtrix_discrimination(base_directory, trial_matrix, onsets_dictionary)

    # Save Behaviour Matrix
    np.save(os.path.join(save_directory, "Behaviour_Matrix.npy"), trial_matrix)





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
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK22.1A/2021_09_26_Discrimination_Behaviour",
    #"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK22.1A/2021_09_27_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK22.1A/2021_09_28_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK22.1A/2021_09_29_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK22.1A/2021_09_30_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK22.1A/2021_10_01_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK22.1A/2021_10_02_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK22.1A/2021_10_03_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK22.1A/2021_10_04_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK22.1A/2021_10_05_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK22.1A/2021_10_06_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK22.1A/2021_10_07_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK22.1A/2021_10_08_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK22.1A/2021_10_09_Discrimination_Behaviour",

    # 7.1B Slow learner
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK7.1B/2021_02_01_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK7.1B/2021_02_02_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK7.1B/2021_02_03_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK7.1B/2021_02_04_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK7.1B/2021_02_05_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK7.1B/2021_02_06_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK7.1B/2021_02_07_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK7.1B/2021_02_08_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK7.1B/2021_02_09_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK7.1B/2021_02_10_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK7.1B/2021_02_11_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK7.1B/2021_02_12_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK7.1B/2021_02_13_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK7.1B/2021_02_14_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK7.1B/2021_02_15_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK7.1B/2021_02_16_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK7.1B/2021_02_17_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK7.1B/2021_02_18_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK7.1B/2021_02_19_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK7.1B/2021_02_20_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK7.1B/2021_02_21_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK7.1B/2021_02_22_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK7.1B/2021_02_23_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK7.1B/2021_02_24_Discrimination_Imaging",

]

session_list = [
r"/media/matthew/Seagate Expansion Drive1/NXAK4.1A/2021_02_02_Discrimination_Imaging",
r"/media/matthew/Seagate Expansion Drive1/NXAK4.1A/2021_02_04_Discrimination_Imaging",
r"/media/matthew/Seagate Expansion Drive1/NXAK4.1A/2021_02_06_Discrimination_Imaging",
r"/media/matthew/Seagate Expansion Drive1/NXAK4.1A/2021_02_08_Discrimination_Imaging",
r"/media/matthew/Seagate Expansion Drive1/NXAK4.1A/2021_02_10_Discrimination_Imaging",
r"/media/matthew/Seagate Expansion Drive1/NXAK4.1A/2021_02_12_Discrimination_Imaging",
r"/media/matthew/Seagate Expansion Drive1/NXAK4.1A/2021_02_14_Discrimination_Imaging",
r"/media/matthew/Seagate Expansion Drive1/NXAK4.1A/2021_02_16_Discrimination_Imaging",
r"/media/matthew/Seagate Expansion Drive1/NXAK4.1A/2021_02_18_Discrimination_Imaging",
r"/media/matthew/Seagate Expansion Drive1/NXAK4.1A/2021_02_23_Discrimination_Imaging",
r"/media/matthew/Seagate Expansion Drive1/NXAK4.1A/2021_02_25_Discrimination_Imaging",
r"/media/matthew/Seagate Expansion Drive1/NXAK4.1A/2021_02_27_Discrimination_Imaging",
r"/media/matthew/Seagate Expansion Drive1/NXAK4.1A/2021_03_01_Discrimination_Imaging",
r"/media/matthew/Seagate Expansion Drive1/NXAK4.1A/2021_03_03_Discrimination_Imaging",
r"/media/matthew/Seagate Expansion Drive1/NXAK4.1A/2021_03_05_Discrimination_Imaging",
]

session_list = [
    r"/media/matthew/Seagate Expansion Drive1/Processed_Widefield_Data/NXAK20.1B/2021_09_28_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive1/Processed_Widefield_Data/NXAK20.1B/2021_09_30_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive1/Processed_Widefield_Data/NXAK20.1B/2021_10_02_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive1/Processed_Widefield_Data/NXAK20.1B/2021_10_04_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive1/Processed_Widefield_Data/NXAK20.1B/2021_10_06_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive1/Processed_Widefield_Data/NXAK20.1B/2021_10_09_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive1/Processed_Widefield_Data/NXAK20.1B/2021_10_11_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive1/Processed_Widefield_Data/NXAK20.1B/2021_10_13_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive1/Processed_Widefield_Data/NXAK20.1B/2021_10_15_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive1/Processed_Widefield_Data/NXAK20.1B/2021_10_17_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive1/Processed_Widefield_Data/NXAK20.1B/2021_10_19_Discrimination_Imaging",
]

for session in session_list:
    create_behaviour_matrix(session)




