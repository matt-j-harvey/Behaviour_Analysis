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
import Get_Stable_Windows_Mirror
import Plot_Behaviour_Matrix


def create_session_list(base_directory):

    sub_directories = os.listdir(base_directory)

    session_list = []

    for directory in sub_directories:
        if "Switching" in directory or "Transition" in directory:
            session_list.append(os.path.join(base_directory,directory))

    return session_list

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





def split_stream_by_context(stimuli_onsets, context_onsets, context_window):

    context_negative_onsets = []
    context_positive_onsets = []

    # Iterate Through Visual 1 Onsets
    for stimuli_onset in stimuli_onsets:
        context = False
        window_start = stimuli_onset
        window_end = stimuli_onset + context_window

        for context_onset in context_onsets:
            if context_onset >= window_start and context_onset <= window_end:
                context = True

        if context == True:
            context_positive_onsets.append(stimuli_onset)
        else:
            context_negative_onsets.append(stimuli_onset)

    return context_negative_onsets, context_positive_onsets



def split_odour_onsets_by_context(visual_1_onsets, visual_2_onsets, odour_1_onsets, odour_2_onsets, following_window_size=5000):

    combined_visual_onsets = visual_1_onsets + visual_2_onsets
    odour_block_stimuli_1, visual_block_stimuli_1 = split_stream_by_context(odour_1_onsets, combined_visual_onsets, following_window_size)
    odour_block_stimuli_2, visual_block_stimuli_2 = split_stream_by_context(odour_2_onsets, combined_visual_onsets, following_window_size)

    onsets_list = [visual_block_stimuli_1, visual_block_stimuli_2, odour_block_stimuli_1, odour_block_stimuli_2]

    return onsets_list




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
    print("AI filename", ai_filename)
    ai_data = load_ai_recorder_file(base_directory + ai_filename)

    # Create Stimuli Dictionary
    stimuli_dictionary = create_stimuli_dictionary()

    # Load Traces
    lick_trace = ai_data[stimuli_dictionary["Lick"]]
    running_trace = ai_data[stimuli_dictionary["Running"]]
    vis_1_trace = ai_data[stimuli_dictionary["Visual 1"]]
    vis_2_trace = ai_data[stimuli_dictionary["Visual 2"]]
    odour_1_trace = ai_data[stimuli_dictionary["Odour 1"]]
    odour_2_trace = ai_data[stimuli_dictionary["Odour 2"]]
    reward_trace = ai_data[stimuli_dictionary["Reward"]]
    relevance_trace = ai_data[stimuli_dictionary["Irrelevance"]]
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

    # Create Some Combined Traces
    combined_odour_trace  = np.max([odour_1_trace, odour_2_trace], axis=0)
    combined_visual_trace = np.max([vis_1_trace,   vis_2_trace],   axis=0)

    # Get Onsets
    vis_1_onsets    = get_step_onsets(vis_1_trace)
    vis_2_onsets    = get_step_onsets(vis_2_trace)
    odour_1_onsets  = get_step_onsets(odour_1_trace)
    odour_2_onsets  = get_step_onsets(odour_2_trace)
    lick_onsets     = get_step_onsets(lick_trace, threshold=lick_threshold, window=10)
    reward_onsets   = get_step_onsets(reward_trace)
    frame_onsets    = get_step_onsets(frame_trace)
    end_onsets      = get_step_onsets(end_trace)


    # In Mirror Context We Need To Split Odour Onsets By Context
    # The Relevance Trace Does not Work
    odour_onsets_by_context = split_odour_onsets_by_context(vis_1_onsets, vis_2_onsets, odour_1_onsets, odour_2_onsets)

    vis_context_odour_1_onsets    = odour_onsets_by_context[0]
    vis_context_odour_2_onsets    = odour_onsets_by_context[1]
    odour_context_odour_1_onsets  = odour_onsets_by_context[2]
    odour_context_odour_2_onsets  = odour_onsets_by_context[3]

    plt.plot(vis_1_trace, c='b')
    plt.plot(vis_2_trace, c='r')
    plt.plot(odour_1_trace, c='g')
    plt.plot(odour_2_trace, c='m')
    plt.plot(end_trace, c='k')

    plt.scatter(vis_context_odour_1_onsets, np.ones(len(vis_context_odour_1_onsets)), c='k')
    plt.scatter(vis_context_odour_2_onsets, np.ones(len(vis_context_odour_2_onsets)), c='k')
    plt.scatter(odour_context_odour_1_onsets, np.ones(len(odour_context_odour_1_onsets)), c='c')
    plt.scatter(odour_context_odour_2_onsets, np.ones(len(odour_context_odour_2_onsets)), c='c')

    plt.show()


    # Get Widefield Frame Indexes
    widefield_frame_onsets = get_frame_indexes(frame_trace)
    np.save(os.path.join(save_directory, "Frame_Times.npy"), widefield_frame_onsets)

    # Get Mousecam Frame Indexes
    mousecam_frame_onsets = get_frame_indexes(mousecam_trace)
    np.save(os.path.join(save_directory, "Mousecam_Frame_Times.npy"), mousecam_frame_onsets)

    # Get Photodiode Times
    photodiode_onsets, photodiode_line = get_step_onsets_photodiode(photodiode_trace, threshold=0.25, window=5)


    onsets_dictionary ={"vis_1_onsets":vis_1_onsets,
                        "vis_2_onsets":vis_2_onsets,
                        "odour_1_onsets":odour_1_onsets,
                        "odour_2_onsets":odour_2_onsets,
                        "lick_onsets":lick_onsets,
                        "reward_onsets":reward_onsets,
                        "vis_context_odour_1_onsets":vis_context_odour_1_onsets,
                        "vis_context_odour_2_onsets":vis_context_odour_2_onsets,
                        "odour_context_odour_1_onsets":odour_context_odour_1_onsets,
                        "odour_context_odour_2_onsets":odour_context_odour_2_onsets,
                        "frame_onsets":frame_onsets,
                        "trial_ends":end_onsets,
                        "photodiode_onsets":photodiode_onsets}


    traces_dictionary ={"lick_trace":lick_trace,
                        "running_trace":running_trace,
                        "vis_1_trace":vis_1_trace,
                        "vis_2_trace":vis_2_trace,
                        "odour_1_trace":odour_1_trace,
                        "odour_2_trace":odour_2_trace,
                        "reward_trace":reward_trace,
                        "relevance_trace":relevance_trace,
                        "combined_odour_trace":combined_odour_trace,
                        "combined_visual_trace":combined_visual_trace,
                        "frame_trace":frame_trace,
                        "end_trace":end_trace,
                        "photodiode_trace":photodiode_trace}


    return onsets_dictionary, traces_dictionary



def get_trial_type(onset, onsets_dictionary):

    odour_context_odour_1_onsets = onsets_dictionary["odour_context_odour_1_onsets"]
    odour_context_odour_2_onsets = onsets_dictionary["odour_context_odour_2_onsets"]
    vis_1_onsets = onsets_dictionary["vis_1_onsets"]
    vis_2_onsets = onsets_dictionary["vis_2_onsets"]

    if onset in vis_1_onsets:
        return 1
    elif onset in vis_2_onsets:
        return 2
    elif onset in odour_context_odour_1_onsets:
        return 3
    elif onset in odour_context_odour_2_onsets:
        return 4


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
    elif trial_type == 3:
        stream = traces_dictionary['odour_1_trace']
    elif trial_type == 4:
        stream = traces_dictionary['odour_2_trace']

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


def get_irrel_details(onset, trial_type, onsets_dictionary, traces_dictionary, irrel_preceeding_window=5000):

    # Get Irrel Offsets:
    vis_context_odour_1_onsets = onsets_dictionary["vis_context_odour_1_onsets"]
    vis_context_odour_2_onsets = onsets_dictionary["vis_context_odour_2_onsets"]
    odour_1_trace = traces_dictionary['odour_1_trace']
    odour_2_trace = traces_dictionary['odour_2_trace']

    odour_1_irrel_offsets = []
    for irrel_odour_1_onset in vis_context_odour_1_onsets:
        odour_1_irrel_offsets.append(get_offset(irrel_odour_1_onset, odour_1_trace))

    odour_2_irrel_offsets = []
    for irrel_odour_2_onset in vis_context_odour_2_onsets:
        odour_2_irrel_offsets.append(get_offset(irrel_odour_2_onset, odour_2_trace))

    preceeded = 0
    irrel_type = np.nan
    irrel_onset = np.nan

    if trial_type == 3 or trial_type == 4:
        return preceeded, irrel_type, irrel_onset

    else:
        window_start = (onset - irrel_preceeding_window)
        window_stop = onset

        irrel_trial_index = 0
        for candidate_irrel_offset in odour_1_irrel_offsets:
            if candidate_irrel_offset > window_start and candidate_irrel_offset < window_stop:
                preceeded = 1
                irrel_type = 3
                irrel_onset = vis_context_odour_1_onsets[irrel_trial_index]
                return preceeded, irrel_type, irrel_onset
            irrel_trial_index += 1

        irrel_trial_index = 0
        for candidate_irrel_offset in odour_2_irrel_offsets:
            if candidate_irrel_offset > window_start and candidate_irrel_offset < window_stop:
                preceeded = 1
                irrel_type = 4
                irrel_onset = vis_context_odour_2_onsets[irrel_trial_index]
                return  preceeded, irrel_type, irrel_onset
            irrel_trial_index += 1

        return preceeded, irrel_type, irrel_onset


def get_irrel_offset(irrel_onset, irrel_type, traces_dictionary):

    if math.isnan(irrel_type):
        return np.nan
    elif irrel_type == 1:
        irrel_trace = traces_dictionary["vis_1_trace"]
    elif irrel_type == 2:
        irrel_trace = traces_dictionary["vis_2_trace"]
    elif irrel_type == 3:
        irrel_trace = traces_dictionary["odour_1_trace"]
    elif irrel_type == 4:
        irrel_trace = traces_dictionary["odour_2_trace"]

    offset = get_offset(irrel_onset, irrel_trace)

    return offset


def get_ignore_irrel(irrel_onset, irrel_offset, traces_dictionary, lick_threshold):

    if math.isnan(irrel_onset) or math.isnan(irrel_offset):
        return np.nan
    else:
        lick_trace = traces_dictionary['lick_trace']
        irrel_lick_trace = lick_trace[irrel_onset:irrel_offset]
        if np.max(irrel_lick_trace) >= lick_threshold:
            return 0
        else:
            return 1


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


def get_photodiode_timings(trial_type, preceeded_by_irrel, stimuli_onset, irrel_onset, onsets_dictionary, traces_dictionary):

    photodiode_onset = None
    photodiode_offset = None

    photodiode_onset_list = onsets_dictionary['photodiode_onsets']
    photodiode_trace = traces_dictionary['photodiode_trace']

    if trial_type == 1 or trial_type == 2:
        photodiode_onset = Widefield_General_Functions.take_closest(photodiode_onset_list, stimuli_onset)
        photodiode_offset = get_offset(photodiode_onset, photodiode_trace, threshold=0.25)
        return photodiode_onset, photodiode_offset

    elif trial_type == 3 or trial_type == 4:
        if preceeded_by_irrel == 1:
            photodiode_onset = Widefield_General_Functions.take_closest(photodiode_onset_list, irrel_onset)
            photodiode_offset = get_offset(photodiode_onset, photodiode_trace, threshold=0.25)
            return photodiode_onset, photodiode_offset
        else:
            return np.nan, np.nan

def classify_trial(onset, onsets_dictionary, traces_dictionary, trial_index, lick_threshold):

    """
    0 trial_index = int, index of trial
    1 trial_type = 1 - rewarded visual, 2 - unrewarded visual, 3 - rewarded odour, 4 - unrewarded odour
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
    preeceded_by_irrel, irrel_type, irrel_onset = get_irrel_details(onset, trial_type, onsets_dictionary, traces_dictionary)
    print("Preceeded by irrel: ", preeceded_by_irrel)

    # Get Irrel Offset
    irrel_offset = get_irrel_offset(irrel_onset, irrel_type, traces_dictionary)

    # Get Ignore Irrel
    ignore_irrel = get_ignore_irrel(irrel_onset, irrel_offset, traces_dictionary, lick_threshold)

    # Get Photodiode Timings
    photodiode_onset, photodiode_offset = get_photodiode_timings(trial_type, preeceded_by_irrel, onset, irrel_onset, onsets_dictionary, traces_dictionary)

    first_in_block = None
    in_block_of_stable_performance = 0
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





def get_block_boudaries(onsets_dictionary):

    vis_1_onsets = onsets_dictionary["vis_1_onsets"]
    vis_2_onsets = onsets_dictionary["vis_2_onsets"]
    odour_context_odour_1_onsets = onsets_dictionary["odour_context_odour_1_onsets"]
    odour_context_odour_2_onsets = onsets_dictionary["odour_context_odour_2_onsets"]

    # Get Visual trial Stimuli,
    vis_context_stimuli = np.concatenate([vis_1_onsets, vis_2_onsets])
    vis_context_stimuli.sort()

    # Get Odour Trial Stimuli
    odour_context_stimuli = np.concatenate([odour_context_odour_1_onsets, odour_context_odour_2_onsets])
    odour_context_stimuli.sort()

    all_onsets = np.concatenate([vis_context_stimuli, odour_context_stimuli])
    all_onsets = np.sort(all_onsets)

    block_boundaries = [0]
    block_types = []

    # Get Initial Block
    if vis_context_stimuli[0] < odour_context_stimuli[0]:
        initial_block = 0
    else:
        initial_block = 1
    block_types.append(initial_block)

    # Get Subsequent Blocks
    current_block = initial_block

    number_of_trials = len(all_onsets)
    for trial in range(1, number_of_trials):

        onset = all_onsets[trial]

        # If Its a Visual Onset
        if onset in vis_context_stimuli:
            if current_block == 1:
                current_block = 0
                block_boundaries.append(trial)
                block_types.append(current_block)

        elif onset in odour_context_stimuli:
            if current_block == 0:
                current_block = 1
                block_boundaries.append(trial)
                block_types.append(current_block)

    #print("Block Boundaires", block_boundaries)
    #print("BLock Types", block_types)
    return block_boundaries, block_types


def add_block_boundaries(trial_matrix, block_boundaries):

    # remove first boundary (first trial)
    block_boundaries = block_boundaries[1:]
    current_block = 0

    number_of_trials = np.shape(trial_matrix)[0]
    for trial_index in range(number_of_trials):
        if trial_index in block_boundaries:
            trial_matrix[trial_index][9] = 1
            current_block += 1
        else:
            trial_matrix[trial_index][9] = 0

        trial_matrix[trial_index][8] = current_block

    return trial_matrix


def add_stable_windows(behaviour_matrix, stable_windows):

    for window in stable_windows:
        for trial in window:
            behaviour_matrix[trial][10] = 1
    return behaviour_matrix



def get_nearest_frame(stimuli_onsets, frame_times):

    #frame_times = frame_onsets.keys()
    nearest_frames = []
    window_size = 50

    if len(stimuli_onsets) > 0:

        #print("Stimuli Onsets", stimuli_onsets)
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


def convert_to_photodiode_onsets(photodiode_onsets, stimuli_onsets):

    adjustment_list = []
    adjusted_onsets_list = []
    for onset in stimuli_onsets:
        adjusted_onset = Widefield_General_Functions.take_closest(photodiode_onsets, onset)
        adjusted_onsets_list.append(adjusted_onset)
        adjustment_list.append(np.abs(adjusted_onset - onset))

    #print("Mean Adjustment", np.mean(adjustment_list))
    return adjusted_onsets_list




def save_onsets(base_directory, behaviour_matrix, selected_trials, onsets_dictionary, save_directory, photodiode_onsets):

    # Load Trials
    Odour_Context_Odour_1_Stable_trials     = selected_trials[0]
    Odour_Context_Odour_2_Stable_trials     = selected_trials[1]
    Visual_Context_Odour_1_Stable_trials    = selected_trials[2]
    Visual_Context_Odour_2_Stable_trials    = selected_trials[3]
    Visual_Expected_Absent_trials           = selected_trials[4]
    Visual_Expected_Present_trials          = selected_trials[5]
    Visual_Not_Expected_Absent_trials       = selected_trials[6]
    Perfect_Switch_Trials_trials            = selected_trials[7]
    Miss_Switch_Trials                      = selected_trials[8]
    Vis_1_cued_trials                       = selected_trials[9]
    Vis_2_cued_trials                       = selected_trials[10]
    Vis_1_not_cued_trials                   = selected_trials[11]
    Vis_2_not_cued_trials                   = selected_trials[12]

    print("Visual Expected Present Trials", Visual_Expected_Present_trials)
    print("Visual expected absent trials", Visual_Expected_Absent_trials)
    print("Visual Not Expected, Not Present Trials", Visual_Not_Expected_Absent_trials)

    # Get Stimuli Times For Each Trial Category
    Odour_Context_Odour_1_Stable_times  = get_times_from_behaviour_matrix(behaviour_matrix, Odour_Context_Odour_1_Stable_trials, 11)
    Odour_Context_Odour_2_Stable_times  = get_times_from_behaviour_matrix(behaviour_matrix, Odour_Context_Odour_2_Stable_trials, 11)
    Visual_Context_Odour_1_Stable_times = get_times_from_behaviour_matrix(behaviour_matrix, Visual_Context_Odour_1_Stable_trials, 13)
    Visual_Context_Odour_2_Stable_times = get_times_from_behaviour_matrix(behaviour_matrix, Visual_Context_Odour_2_Stable_trials, 13)
    Visual_Expected_Absent_times        = get_times_from_behaviour_matrix(behaviour_matrix, Visual_Expected_Absent_trials, 12)
    Visual_Expected_Present_times       = get_times_from_behaviour_matrix(behaviour_matrix, Visual_Expected_Present_trials, 14)
    Visual_Not_Expected_Absent_times    = get_times_from_behaviour_matrix(behaviour_matrix, Visual_Not_Expected_Absent_trials, 12)
    Perfect_Switch_Trials_times         = get_times_from_behaviour_matrix(behaviour_matrix, Perfect_Switch_Trials_trials, 12)
    Miss_Switch_times                   = get_times_from_behaviour_matrix(behaviour_matrix, Miss_Switch_Trials, 12)
    Vis_1_cued_times                    = get_times_from_behaviour_matrix(behaviour_matrix, Vis_1_cued_trials, 11)
    Vis_2_cued_times                    = get_times_from_behaviour_matrix(behaviour_matrix, Vis_2_cued_trials, 11)
    Vis_1_not_cued_times                = get_times_from_behaviour_matrix(behaviour_matrix, Vis_1_not_cued_trials, 11)
    Vis_2_not_cued_times                = get_times_from_behaviour_matrix(behaviour_matrix, Vis_2_not_cued_trials, 11)

    # Load Frame Onsets
    frame_onsets = onsets_dictionary['frame_onsets']

    # Get Frames For Each Stimuli Category
    Odour_Context_Odour_1_Stable_onsets     = get_nearest_frame(Odour_Context_Odour_1_Stable_times,    frame_onsets)
    Odour_Context_Odour_2_Stable_onsets     = get_nearest_frame(Odour_Context_Odour_2_Stable_times,    frame_onsets)
    Visual_Context_Odour_1_Stable_onsets    = get_nearest_frame(Visual_Context_Odour_1_Stable_times,   frame_onsets)
    Visual_Context_Odour_2_Stable_onsets    = get_nearest_frame(Visual_Context_Odour_2_Stable_times,   frame_onsets)
    print("Visual expected absent times", Visual_Expected_Absent_times)
    Visual_Expected_Absent_onsets           = get_nearest_frame(Visual_Expected_Absent_times,          frame_onsets)
    Visual_Expected_Present_onsets          = get_nearest_frame(Visual_Expected_Present_times,         frame_onsets)
    Visual_Not_Expected_Absent_onsets       = get_nearest_frame(Visual_Not_Expected_Absent_times,      frame_onsets)
    Perfect_Switch_Trials_onsets            = get_nearest_frame(Perfect_Switch_Trials_times,           frame_onsets)
    Miss_Switch_onsets                      = get_nearest_frame(Miss_Switch_times,                     frame_onsets)
    Vis_1_cued_onsets                       = get_nearest_frame(Vis_1_cued_times,                      frame_onsets)
    Vis_2_cued_onsets                       = get_nearest_frame(Vis_2_cued_times,                      frame_onsets)
    Vis_1_not_cued_onsets                   = get_nearest_frame(Vis_1_not_cued_times,                  frame_onsets)
    Vis_2_not_cued_onsets                   = get_nearest_frame(Vis_2_not_cued_times,                  frame_onsets)

    # Save Onsets
    np.save(os.path.join(save_directory, "Odour_Context_Odour_1_Stable_onsets.npy"),    Odour_Context_Odour_1_Stable_onsets)
    np.save(os.path.join(save_directory, "Odour_Context_Odour_2_Stable_onsets.npy"),    Odour_Context_Odour_2_Stable_onsets)
    np.save(os.path.join(save_directory, "Visual_Context_Odour_1_Stable_onsets.npy"),   Visual_Context_Odour_1_Stable_onsets)
    np.save(os.path.join(save_directory, "Visual_Context_Odour_2_Stable_onsets.npy"),   Visual_Context_Odour_2_Stable_onsets)
    np.save(os.path.join(save_directory, "Visual_Expected_Absent_onsets.npy"),          Visual_Expected_Absent_onsets)
    np.save(os.path.join(save_directory, "Visual_Expected_Present_onsets.npy"),         Visual_Expected_Present_onsets)
    np.save(os.path.join(save_directory, "Visual_Not_Expected_Absent_onsets.npy"),      Visual_Not_Expected_Absent_onsets)
    np.save(os.path.join(save_directory, "Perfect_Switch_Trials_onsets.npy"),           Perfect_Switch_Trials_onsets)
    np.save(os.path.join(save_directory, "Miss_Switch_onsets.npy"),                     Miss_Switch_onsets)
    np.save(os.path.join(save_directory, "Vis_1_cued_onsets.npy"),                      Vis_1_cued_onsets)
    np.save(os.path.join(save_directory, "Vis_2_cued_onsets.npy"),                      Vis_2_cued_onsets)
    np.save(os.path.join(save_directory, "Vis_1_not_cued_onsets.npy"),                  Vis_1_not_cued_onsets)
    np.save(os.path.join(save_directory, "Vis_2_not_cued_onsets.npy"),                  Vis_2_not_cued_onsets)


def get_selected_trials(behaviour_matrix):

    """
    Stable Trials
    Odour_Context_Odour_1_Stable - correct, in stable block, not first in block
    Odour_Context_Odour_2_Stable - correct, in stable block, not first in block
    Visual_Context_Odour_1_Stable - correct, in stable block, not first in block, ignored irrel
    Visual_Context_Odour_2_Stable - correct, in stable block, not first in block, ignored irrel

    Absence of Expected Odour
    Visual_Expected_Present – Odour 2, correct, preceeded by irrel, ignore irrel
    Visual_Not_Expected_Absent – visual block, end of vis 2, correct,
    Visual_Expected_Absent - first in visual block, vis 1, miss
    Perfect_Switch_Trials  – first in odour block, odour 1 miss, next trial correct
    Miss_Switch_Trials - first in odour block, odour 1 miss, miss, next trial incorrect

    Cued v Non-Cued Visual
    Vis_1_cued - Visual 1 - correct - in stable block - preceeded by irrel
    Vis_2_cued - Visual 2 - correct - in stable block - preceeded by irrel
    Vis_1_not_cued - Visual 2 - correct - in stable block - not preceeded by irrel
    Vis_2_not_cued - Visual 2 - correct - in stable block - not preceeded by irrel

    """

    # Get Selected Trials
    Odour_Context_Odour_1_Stable_trials = []
    Odour_Context_Odour_2_Stable_trials = []
    Visual_Context_Odour_1_Stable_trials = []
    Visual_Context_Odour_2_Stable_trials = []

    Visual_Expected_Absent_trials = []
    Visual_Expected_Present_trials = []
    Visual_Not_Expected_Absent_trials = []
    Perfect_Switch_Trials_trials = []
    Miss_Switch_Trials = []

    Vis_1_cued_trials = []
    Vis_2_cued_trials = []
    Vis_1_not_cued_trials = []
    Vis_2_not_cued_trials = []

    # Iterate Through Each Trial
    number_of_trials = np.shape(behaviour_matrix)[0]
    for trial_index in range(number_of_trials):

        trial_is_correct    = behaviour_matrix[trial_index][3]
        in_stable_window    = behaviour_matrix[trial_index][10]
        trial_type          = behaviour_matrix[trial_index][1]
        first_in_block      = behaviour_matrix[trial_index][9]
        ignore_irrel        = behaviour_matrix[trial_index][7]
        preeceeded_by_irrel = behaviour_matrix[trial_index][5]


        # Check If Trial Is Stable
        if trial_is_correct and in_stable_window and not first_in_block:

            # If We Are In Odour Block
            if trial_type == 3:
                Odour_Context_Odour_1_Stable_trials.append(trial_index)

            elif trial_type == 4:
                Odour_Context_Odour_2_Stable_trials.append(trial_index)

            # If We Are In Visual Block
            elif trial_type == 1 or trial_type == 2:

                # Check We Also Ignored The Odour
                if ignore_irrel:
                    irrel_type = behaviour_matrix[trial_index][6]

                    if irrel_type == 3:
                        Visual_Context_Odour_1_Stable_trials.append(trial_index)
                    elif irrel_type == 4:
                        Visual_Context_Odour_2_Stable_trials.append(trial_index)


        # Check If Trial is A Perfect Transition Trial
        # Odour block
        # Odour 1
        # First in block
        # Miss
        # Next trial correct
        if trial_type == 3 or trial_type == 4:

            if first_in_block:

                Visual_Expected_Absent_trials.append(trial_index)

                if trial_index < number_of_trials-1:

                    following_trial_correct = behaviour_matrix[trial_index + 1][3]

                    if not trial_is_correct:


                        if following_trial_correct:
                            Perfect_Switch_Trials_trials.append(trial_index)

                        if not following_trial_correct:
                            Miss_Switch_Trials.append(trial_index)


        # Check If Is Visual Expected and Present
        # Visual 2, correct, stable, preceeded by irrel, ignore irrel, not first in block
        if trial_type == 2 and trial_is_correct and not first_in_block:
            print("Potential Correct Visual BLock Trial")
            print(preeceeded_by_irrel)
            if preeceeded_by_irrel and ignore_irrel:
                print("Ignored Irrel")
                Visual_Expected_Present_trials.append(trial_index)

        # Check If Visual Not Expected Not Present
        # Odour block - Odour 2 correct
        if trial_type == 4 and trial_is_correct:
            Visual_Not_Expected_Absent_trials.append(trial_index)

        # Check If Cued
        if trial_type == 1 or trial_type == 2 and trial_is_correct and ignore_irrel and in_stable_window:

            if trial_type == 1 and preeceeded_by_irrel:
                Vis_1_cued_trials.append(trial_index)

            if trial_type == 2 and preeceeded_by_irrel:
                Vis_2_cued_trials.append(trial_index)

            if trial_type == 1 and not preeceeded_by_irrel:
                Vis_1_not_cued_trials.append(trial_index)

            if trial_type == 2 and not preeceeded_by_irrel:
                Vis_2_not_cued_trials.append(trial_index)

    selected_trials_list = [
        Odour_Context_Odour_1_Stable_trials,
        Odour_Context_Odour_2_Stable_trials,
        Visual_Context_Odour_1_Stable_trials,
        Visual_Context_Odour_2_Stable_trials,

        Visual_Expected_Absent_trials,
        Visual_Expected_Present_trials,
        Visual_Not_Expected_Absent_trials,
        Perfect_Switch_Trials_trials,
        Miss_Switch_Trials,

        Vis_1_cued_trials,
        Vis_2_cued_trials,
        Vis_1_not_cued_trials,
        Vis_2_not_cued_trials,
    ]

    return selected_trials_list



def get_step_onsets_photodiode(trace, threshold=1, window=10):

    state = 0
    number_of_timepoints = len(trace)
    onset_times = []
    time_below_threshold = 0

    onset_line = []

    for timepoint in range(number_of_timepoints-window):
        if state == 0:
            if trace[timepoint] > threshold and trace[timepoint+window] > threshold:
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

    return onset_times, onset_line



def create_behaviour_matrix(base_directory, behaviour_only=False):

    # Get AI Filename
    ai_filename = get_ai_filename(base_directory)

    # Load Lick Threshold
    #lick_threshold = np.load(os.path.join(base_directory, "Lick_Threshold.npy"))
    lick_threshold = 0.5

    print("Lick Threshold : ", lick_threshold)


    # Create Save Directory
    save_directory = os.path.join(base_directory, "Stimuli_Onsets")
    if not os.path.exists(save_directory):
        os.mkdir(save_directory)

    # Get Trace and Onsets Dictionary
    onsets_dictionary, traces_dictionary = extract_onsets(base_directory, ai_filename, save_directory, lick_threshold=lick_threshold, visualise_lick_threshold=True)

    """
    onsets_dictionary ={"vis_1_onsets":vis_1_onsets,
                        "vis_2_onsets":vis_2_onsets,
                        "odour_1_onsets":odour_1_onsets,
                        "odour_2_onsets":odour_2_onsets,
                        "lick_onsets":lick_onsets,
                        "reward_onsets":reward_onsets,
                        "vis_context_odour_1_onsets":vis_context_odour_1_onsets,
                        "vis_context_odour_2_onsets":vis_context_odour_2_onsets,
                        "odour_context_odour_1_onsets":odour_context_odour_1_onsets,
                        "odour_context_odour_2_onsets":odour_context_odour_2_onsets,
                        "frame_onsets":frame_onsets,
                        "trial_ends":end_onsets,
                        "photodiode_onsets":photodiode_onsets}
    """


    # Create Trial Onsets List
    odour_context_odour_1_onsets = onsets_dictionary["odour_context_odour_1_onsets"]
    odour_context_odour_2_onsets = onsets_dictionary["odour_context_odour_2_onsets"]
    vis_1_onsets = onsets_dictionary["vis_1_onsets"]
    vis_2_onsets = onsets_dictionary["vis_2_onsets"]
    trial_onsets = odour_context_odour_1_onsets + odour_context_odour_2_onsets + vis_1_onsets + vis_2_onsets
    trial_onsets.sort()

    # Classify Trials
    trial_matrix = []
    trial_index = 0
    for trial in trial_onsets:
        trial_vector = classify_trial(trial, onsets_dictionary, traces_dictionary, trial_index, lick_threshold=lick_threshold)
        trial_matrix.append(trial_vector)
        trial_index += 1
    trial_matrix = np.array(trial_matrix)

    # Add Block Boundaries
    block_boundaries, block_types = get_block_boudaries(onsets_dictionary)
    trial_matrix = add_block_boundaries(trial_matrix, block_boundaries)

    # Get Stable Windows - To Do
    stable_windows = Get_Stable_Windows_Mirror.get_stable_windows(trial_matrix)
    trial_matrix = add_stable_windows(trial_matrix, stable_windows)

    # Get Selected Trials
    selected_trials = get_selected_trials(trial_matrix)

    # Print Behaviour Matrix
    #print_behaviour_matrix(trial_matrix)

    # Get Photodiode Onsets
    photodiode_onsets = onsets_dictionary['photodiode_onsets']

    # Save Trials
    if not behaviour_only:
        save_onsets(base_directory, trial_matrix, selected_trials, onsets_dictionary, save_directory, photodiode_onsets)

    # Plot Behaviour Matrix
    Plot_Behaviour_Matrix.plot_behaviour_maxtrix(base_directory, trial_matrix, onsets_dictionary, block_boundaries, stable_windows, selected_trials)

    # Save Behaviour Matrix
    np.save(os.path.join(save_directory, "Behaviour_Matrix.npy"), trial_matrix)




session_list = ["/media/matthew/External_Harddrive_1/Processed_Widefield_Data/Beverly/2022_05_16_Mirror_Imaging",
                "/media/matthew/External_Harddrive_1/Processed_Widefield_Data/Beverly/2022_05_18_Mirror_Imaging",
                "/media/matthew/External_Harddrive_1/Processed_Widefield_Data/Beverly/2022_05_23_mirror_imaging",
                "/media/matthew/External_Harddrive_1/Processed_Widefield_Data/Beverly/2022_05_27_mirror_imaging"]

for session in session_list:
    create_behaviour_matrix(session, behaviour_only=False)


