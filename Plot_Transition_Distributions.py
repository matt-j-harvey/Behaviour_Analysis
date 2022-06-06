import numpy as np
import matplotlib.pyplot as plt
import os
import math
import matplotlib.patches as mpatches


def remove_nans_from_list(original_list):

    new_list = []
    for item in original_list:
        print(item, math.isnan(item))
        if math.isnan(item) == False:
            new_list.append(item)
    return new_list

def get_group_distribution(session_list, direction):

    group_distribution = []

    for session in session_list:

        # Load Performance Dictionary
        performance_dictionary = np.load(os.path.join(session, "Behavioural_Measures", "Performance_Dictionary.npy"), allow_pickle=True)[()]

        # Get distribution
        session_distribution = performance_dictionary[direction + "_transition_distribution"]
        print("Session dsitribution", session_distribution)
        group_distribution = group_distribution + session_distribution

    return group_distribution


def plot_transition_trials_histogram(control_session_list, mutant_session_list, direction="odour_to_visual"):

    # Get Group Distributions
    control_transition_distribution = get_group_distribution(control_session_list, direction)
    mutant_transition_distribution = get_group_distribution(mutant_session_list, direction)

    print("Control Distribution", control_transition_distribution)

    # Get Bins
    control_transition_distribution_set = set(control_transition_distribution)
    print("set", control_transition_distribution_set)
    mutant_transition_distribution_set = set(mutant_transition_distribution)
    control_transition_distribution_set = remove_nans_from_list(control_transition_distribution_set)
    mutant_transition_distribution_set = remove_nans_from_list(mutant_transition_distribution_set)
    control_bins = list(range(int(np.max(control_transition_distribution_set) + 2)))
    mutant_bins = list(range(int(np.max(mutant_transition_distribution_set) + 2)))

    print("Contol bins", control_bins)
    # Get X Ticks
    x_ticks = list(range(int(np.max(control_bins + mutant_bins))))

    # Plot Data
    plt.title("Transition Trials Distribution")
    plt.hist(control_transition_distribution, bins=control_bins, color='b', alpha=0.5, density=True)
    plt.hist(mutant_transition_distribution, bins=mutant_bins, color='g', alpha=0.5, density=True)
    plt.xticks(x_ticks)
    plt.ylabel("Count")

    if direction == "odour_to_visual":
        plt.xlabel("Missed Rewarded Visual Gratings")
    elif direction == "visual_to_odour":
        plt.xlabel("Irrel Vis 1 Licked To")

    # Add Legends
    blue_patch = mpatches.Patch(color='blue', label='Controls')
    green_patch = mpatches.Patch(color='green', label='Mutants')
    ax = plt.gca()
    ax.legend(handles=[blue_patch, green_patch])

    plt.show()


session_list = [
    r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Controls/4.1B/2021_04_02_Transition_Imaging",
    r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Controls/4.1B/2021_04_05_Transition_Behaviour",
    r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Controls/4.1B/2021_04_08_Transition_Imaging",
    r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Controls/4.1B/2021_04_09_Transition_Behaviour",
    r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Controls/4.1B/2021_04_10_Transition_Imaging"
]
plot_transition_trials_histogram(session_list, session_list, direction="odour_to_visual")
plot_transition_trials_histogram(session_list, session_list, direction="visual_to_odour")