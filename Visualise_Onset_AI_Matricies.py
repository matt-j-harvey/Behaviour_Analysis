
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


def plot_average_ai_trace(base_directory, ai_matrix, stimuli_dictionary):


    # Extract Traces
    stimuli_dictionary = create_stimuli_dictionary()
    vis_1_trace     = ai_matrix[stimuli_dictionary["Visual 1"]]
    vis_2_trace     = ai_matrix[stimuli_dictionary["Visual 2"]]
    odour_1_trace   = ai_matrix[stimuli_dictionary["Odour 1"]]
    odour_2_trace   = ai_matrix[stimuli_dictionary["Odour 2"]]
    lick_trace      = ai_matrix[stimuli_dictionary["Lick"]]
    running_trace   = ai_matrix[stimuli_dictionary["Running"]]

    # Create Save Directory
    save_directory = os.path.join(base_directory, "Stimuli_Onsets", "Average_AI_Traces")
    if not os.path.exists(save_directory):
        os.mkdir(save_directory)

    # Get Mean Traces
    vis_1_mean, vis_1_upper_bound, vis_1_lower_bound = get_average_ai_trace(vis_1_trace, trial_start_list, trial_stop_list)
    vis_2_mean, vis_2_upper_bound, vis_2_lower_bound = get_average_ai_trace(vis_2_trace, trial_start_list, trial_stop_list)
    odour_1_mean, odour_1_upper_bound, odour_1_lower_bound = get_average_ai_trace(odour_1_trace, trial_start_list, trial_stop_list)
    odour_2_mean, odour_2_upper_bound, odour_2_lower_bound = get_average_ai_trace(odour_2_trace, trial_start_list, trial_stop_list)
    lick_mean, lick_upper_bound, lick_lower_bound = get_average_ai_trace(lick_trace, trial_start_list, trial_stop_list)
    running_mean, running_upper_bound, running_lower_bound = get_average_ai_trace(running_trace, trial_start_list, trial_stop_list)

    # Plot These
    figure_1 = plt.figure(figsize=(12, 7))
    axis_1 = figure_1.add_subplot(1, 1, 1)
    x_values = np.linspace(start=start_window * 36, stop=stop_window * 36, num=minimum_duration)

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


def visualise_all_onsets(session_list, onset_file_list):

    for base_directory in session_list:

        # Load Downsampled AI File
        downsampled_ai_data = np.load(os.path.join(base_directory, "Downsampled_AI_Matrix_Framewise.npy"))

        for onset_file in onset_file_list:
            onset_list = np.load(os.path.join(base_directory, "Stimuli_Onsets", onset_file))






session_list = [

    #r"/media/matthew/Expansion/Widefield_Analysis/NXAK7.1B/2021_03_23_Transition_Imaging",
    #r"/media/matthew/Expansion/Widefield_Analysis/NXAK7.1B/2021_03_31_Transition_Imaging",
    #r"/media/matthew/Expansion/Widefield_Analysis/NXAK7.1B/2021_04_02_Transition_Imaging",

    #"/media/matthew/Expansion/Widefield_Analysis/NXAK4.1B/2021_04_08_Transition_Imaging",
    #"/media/matthew/Expansion/Widefield_Analysis/NXAK4.1B/2021_04_02_Transition_Imaging",
    #"/media/matthew/Expansion/Widefield_Analysis/NXAK4.1B/2021_04_10_Transition_Imaging",

    "/media/matthew/Expansion/Widefield_Analysis/NXAK22.1A/2021_10_29_Transition_Imaging",
    "/media/matthew/Expansion/Widefield_Analysis/NXAK22.1A/2021_11_03_Transition_Imaging",
    "/media/matthew/Expansion/Widefield_Analysis/NXAK22.1A/2021_11_05_Transition_Imaging",

    "/media/matthew/Expansion/Widefield_Analysis/NXAK14.1A/2021_06_13_Transition_Imaging",  # not yet uploaded
    "/media/matthew/Expansion/Widefield_Analysis/NXAK14.1A/2021_06_15_Transition_Imaging",  # not yet uploaded
    "/media/matthew/Expansion/Widefield_Analysis/NXAK14.1A/2021_06_17_Transition_Imaging",  # motion corrected matches
]
