import mat73
import os
import numpy as np
import matplotlib.pyplot as plt



def smooth_delta_f_matrix(delta_f_maxtrix):

    kernel_size = 5
    kernel = np.ones(kernel_size) / kernel_size
    smoothed_delta_f = []

    for trace in delta_f_maxtrix:
        smoothed_trace = np.convolve(trace, kernel, mode='same')
        smoothed_delta_f.append(smoothed_trace)

    smoothed_delta_f = np.array(smoothed_delta_f)
    return smoothed_delta_f



def normalise_delta_f_matrix(delta_f_matrix):

    delta_f_matrix = np.transpose(delta_f_matrix)
    # Normalise Each Neuron to Min 0, Max 1

    # Subtract Min To Get Min = 0
    min_vector = np.min(delta_f_matrix, axis=0)
    delta_f_matrix = np.subtract(delta_f_matrix, min_vector)

    # Divide By Max To Get Max = 1
    max_vector = np.max(delta_f_matrix, axis=0)
    delta_f_matrix = np.divide(delta_f_matrix, max_vector)

    delta_f_matrix = np.transpose(delta_f_matrix)
    delta_f_matrix = np.nan_to_num(delta_f_matrix)
    return delta_f_matrix


def load_matlab_sessions(base_directory):

    # Iterates Through Directory and Returns All .mat Files

    matlab_file_list = []
    all_files = os.listdir(base_directory)
    for file in all_files:
        if file[-3:] == "mat":
            matlab_file_list.append(os.path.join(base_directory, file))

    return matlab_file_list



def get_perfect_switch_trials(expected_odour_trials, perfect_switch_list):

    perfect_switch_indicies = []

    number_of_trials = len(expected_odour_trials)
    for trial_index in range(number_of_trials):

        if perfect_switch_list[trial_index] == 1:
            perfect_switch_indicies.append(expected_odour_trials[trial_index])

    return perfect_switch_indicies


def get_trial_average():




# Load Matlab Data
base_directory = "/home/matthew/Documents/Nick_Population_Analysis_Data/python_export/Best_switching_sessions_all_sites"
matlab_sessions = load_matlab_sessions(base_directory)

for session in matlab_sessions:

    # Switch Trials
    # Perfect Switch Trials - When Odour would be expected to arrive - minus 1.5 seconds? (Check Interval With Nick) (Check its only the first Trial with Dylan)
    # Visual Context (No Odour, No Expectation) - V2 trials at the end of a visual block, before switch (Check Alignment with Dylan) ?Also Minus 1.5
    # Stable Odour also Minus 1.5 (Ask Dylan To Make This Only Vis 2)

    # Extract Matlab Data
    matlab_data = mat73.loadmat(os.path.join(base_directory, session))['matlab_save_data']
    mismatch_trials = matlab_data['mismatch_trials']
    expected_odour_trials = mismatch_trials['exp_odour'][0]
    is_switch_perfect = mismatch_trials['perfect_switch']

    # Load Relevant Trials
    perfect_switch_trials = get_perfect_switch_trials(expected_odour_trials, is_switch_perfect)
    stable_visual_context = mismatch_trials['no_odour'][0]
    stable_odour_context = mismatch_trials['exp_odour'][0]

    # Load and Preprocess Delta F
    delta_f_matrix = matlab_data['dF']
    delta_f_matrix = np.nan_to_num(delta_f_matrix)
    #delta_f_matrix = smooth_delta_f_matrix(delta_f_matrix)
    #delta_f_matrix = normalise_delta_f_matrix(delta_f_matrix)


    # Get Trial Averages



