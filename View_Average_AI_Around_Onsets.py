import numpy as np
import matplotlib.pyplot as plt
import tables
import os


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
            ai_filename = original_filename
            print("Ai filename is: ", ai_filename)
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





def get_average_ai_trace(trace, trial_start_list, trial_stop_list):

    number_of_trials = len(trial_start_list)

    trace_tensor = []

    for trial_index in range(number_of_trials):
        trial_start = trial_start_list[trial_index]
        trial_stop = trial_stop_list[trial_index]
        trial_data = trace[trial_start:trial_stop]
        trace_tensor.append(trial_data)

    trace_tensor = np.array(trace_tensor)
    average_trace = np.mean(trace_tensor, axis=0)
    trace_sd = np.std(trace_tensor, axis=0)
    
    trace_sd_upper_bound = np.add(average_trace, trace_sd)
    trace_sd_lower_bound = np.subtract(average_trace, trace_sd)
    
    return average_trace, trace_sd_upper_bound, trace_sd_lower_bound


def invert_dictionary(dictionary):
    inv_map = {v: k for k, v in dictionary.items()}
    return inv_map

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


def normalise_ai_matrix(ai_matrix):

    ai_matrix = np.transpose(ai_matrix)

    # Subtract Mins
    min_vector = np.min(ai_matrix, axis=0)
    ai_matrix = np.subtract(ai_matrix, min_vector)

    # Divide by Max
    max_vector = np.max(ai_matrix, axis=0)
    ai_matrix = np.divide(ai_matrix, max_vector)

    ai_matrix = np.transpose(ai_matrix)
    return ai_matrix


def get_standard_start_stop_times(onset_list, start_window, stop_window, frame_times, ai_matrix):

    number_of_timepoints = np.shape(ai_matrix)[1]
    trial_start_list = []
    trial_duration_list = []

    # First Get Durations
    for onset in onset_list:
        onset_frame = onset + start_window

        if onset_frame > 0:
            trial_start = frame_times[onset_frame]

            if onset + stop_window in frame_times:
                trial_stop = frame_times[onset + stop_window]

            if trial_start > 0 and trial_stop < number_of_timepoints:
                trial_duration = trial_stop - trial_start
                trial_duration_list.append(trial_duration)
                trial_start_list.append(trial_start)

    # Get Minimum Duration
    minimum_duration = np.min(trial_duration_list)

    # Now Get Standard Trial Stops
    trial_stop_list = []
    for start_time in trial_start_list:
        trial_stop_list.append(start_time + minimum_duration)

    return trial_start_list, trial_stop_list, minimum_duration


def plot_average_ai_trace(base_directory, ai_matrix, onsets_file, start_window=-84, stop_window=139):

    # Load Onsets
    onset_list = np.load(os.path.join(base_directory, "Stimuli_Onsets", onsets_file))
    if len(onset_list) == 0:
        return False

    # Load Frame Times
    frame_times = np.load(os.path.join(base_directory, "Stimuli_Onsets", "Frame_Times.npy"), allow_pickle=True)[()]
    frame_times = invert_dictionary(frame_times)

    # Get Trial Starts and Stops
    trial_start_list, trial_stop_list, minimum_duration = get_standard_start_stop_times(onset_list, start_window, stop_window, frame_times, ai_matrix)

    # Extract Traces
    stimuli_dictionary = create_stimuli_dictionary()
    vis_1_trace = ai_matrix[stimuli_dictionary["Visual 1"]]
    vis_2_trace = ai_matrix[stimuli_dictionary["Visual 2"]]
    odour_1_trace = ai_matrix[stimuli_dictionary["Odour 1"]]
    odour_2_trace = ai_matrix[stimuli_dictionary["Odour 2"]]
    lick_trace = ai_matrix[stimuli_dictionary["Lick"]]
    running_trace = ai_matrix[stimuli_dictionary["Running"]]

    # Create Save Directory
    save_directory = os.path.join(base_directory, "Stimuli_Onsets", "Average_AI_Traces")
    if not os.path.exists(save_directory):
        os.mkdir(save_directory)
        
    # Get Mean Traces
    vis_1_mean, vis_1_upper_bound, vis_1_lower_bound        = get_average_ai_trace(vis_1_trace, trial_start_list, trial_stop_list)
    vis_2_mean, vis_2_upper_bound, vis_2_lower_bound        = get_average_ai_trace(vis_2_trace, trial_start_list, trial_stop_list)
    odour_1_mean, odour_1_upper_bound, odour_1_lower_bound  = get_average_ai_trace(odour_1_trace, trial_start_list, trial_stop_list)
    odour_2_mean, odour_2_upper_bound, odour_2_lower_bound  = get_average_ai_trace(odour_2_trace, trial_start_list, trial_stop_list)
    lick_mean, lick_upper_bound, lick_lower_bound           = get_average_ai_trace(lick_trace, trial_start_list, trial_stop_list)
    running_mean, running_upper_bound, running_lower_bound  = get_average_ai_trace(running_trace, trial_start_list, trial_stop_list)

    # Plot These
    figure_1 = plt.figure(figsize=(12,7))
    axis_1 = figure_1.add_subplot(1,1,1)
    x_values = np.linspace(start=start_window * 36, stop=stop_window*36, num=minimum_duration)

    axis_1.plot(x_values, vis_1_mean, c='b', label="Vis 1")
    axis_1.plot(x_values, vis_2_mean, c='r', label="Vis 2")
    axis_1.plot(x_values, odour_1_mean, c='g', label="Odour 1")
    axis_1.plot(x_values, odour_2_mean, c='m', label="Odour 2")
    axis_1.plot(x_values, running_mean, c='saddlebrown', label="Running")
    axis_1.plot(x_values, lick_mean, color='orange', label="Licking")

    # Shade SDs
    axis_1.fill_between(x=x_values, y1=vis_1_lower_bound, y2=vis_1_upper_bound, color='b', alpha=0.2)
    axis_1.fill_between(x=x_values, y1=vis_2_lower_bound, y2=vis_2_upper_bound, color='r', alpha=0.2)
    axis_1.fill_between(x=x_values, y1=odour_1_lower_bound, y2=odour_1_upper_bound, color='g', alpha=0.2)
    axis_1.fill_between(x=x_values, y1=odour_2_lower_bound, y2=odour_2_upper_bound, color='m', alpha=0.2)
    axis_1.fill_between(x=x_values, y1=running_lower_bound, y2=running_upper_bound, color='saddlebrown', alpha=0.2)
    axis_1.fill_between(x=x_values, y1=lick_lower_bound, y2=lick_upper_bound, color='orange', alpha=0.2)

    # Set Title
    plot_title = onsets_file.replace(".npy", "")
    plt.title(plot_title)

    # Add Line At Stimuli Onset
    axis_1.axvline(x=0, c='k', linestyle='--')

    # Put a legend to the right of the current axis
    box = axis_1.get_position()
    axis_1.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    axis_1.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    # Save Figure
    plt.savefig(os.path.join(save_directory, plot_title + ".svg"))
    plt.show()


def get_onset_file_list(base_directory):

    onset_file_list = []
    stimuli_onset_files = os.listdir(os.path.join(base_directory, "Stimuli_Onsets"))

    for file_name in stimuli_onset_files:
        if "_onsets.npy" in file_name:
            onset_file_list.append(file_name)

    return onset_file_list


def plot_average_traces_for_all_onsets(base_directory):

    # Load AI Matrix
    ai_filename = get_ai_filename(base_directory)
    ai_matrix = load_ai_recorder_file(os.path.join(base_directory, ai_filename))

    # Normalise AI Matrix
    ai_matrix = normalise_ai_matrix(ai_matrix)

    # Get List Of Conditions
    onset_file_list = get_onset_file_list(base_directory)

    for condition in onset_file_list:
        plot_average_ai_trace(base_directory, ai_matrix, condition)



session_list = [

    "/media/matthew/Expansion/Widefield_Analysis/NXAK4.1B/2021_04_08_Transition_Imaging",
    "/media/matthew/Expansion/Widefield_Analysis/NXAK4.1B/2021_04_02_Transition_Imaging",
    "/media/matthew/Expansion/Widefield_Analysis/NXAK4.1B/2021_04_10_Transition_Imaging",

    r"/media/matthew/Expansion/Widefield_Analysis/NXAK7.1B/2021_03_23_Transition_Imaging",
    r"/media/matthew/Expansion/Widefield_Analysis/NXAK7.1B/2021_03_31_Transition_Imaging",
    r"/media/matthew/Expansion/Widefield_Analysis/NXAK7.1B/2021_04_02_Transition_Imaging",

    "/media/matthew/Expansion/Widefield_Analysis/NXAK22.1A/2021_10_29_Transition_Imaging",
    "/media/matthew/Expansion/Widefield_Analysis/NXAK22.1A/2021_11_03_Transition_Imaging",
    "/media/matthew/Expansion/Widefield_Analysis/NXAK22.1A/2021_11_05_Transition_Imaging",

    "/media/matthew/Expansion/Widefield_Analysis/NXAK14.1A/2021_06_13_Transition_Imaging",
    "/media/matthew/Expansion/Widefield_Analysis/NXAK14.1A/2021_06_15_Transition_Imaging",
    "/media/matthew/Expansion/Widefield_Analysis/NXAK14.1A/2021_06_17_Transition_Imaging",
]


for base_directory in session_list:

    plot_average_traces_for_all_onsets(base_directory)



