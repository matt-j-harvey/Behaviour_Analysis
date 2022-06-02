import os
import math
import numpy as np
import sys
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn
import seaborn as sns
import pandas as pd


import Create_Behaviour_Matrix
import Behaviour_Analysis_Functions
import Transition_Analysis



def create_behaviour_matricies(mouse_directory, lick_threshold):

    # Load Transition Sessions
    behavioural_sessions = os.listdir(mouse_directory)
    transition_session_list = []
    for session in behavioural_sessions:
        if 'Transition' in session:
            transition_session_list.append(session)

    for session in transition_session_list:
        Create_Behaviour_Matrix.create_behaviour_matrix(os.path.join(mouse_directory, session), lick_threshold=lick_threshold, behaviour_only=True)



def analyse_transition_session(base_directory):

    # Load Behaviour Matrix
    behaviour_matrix = np.load(os.path.join(base_directory, "Stimuli_Onsets", "Behaviour_Matrix.npy"), allow_pickle=True)

    # Get Visual Discrimination
    vis_trial_outcome_list, vis_hits, vis_misses, vis_false_alarms, vis_correct_rejections = Behaviour_Analysis_Functions.analyse_visual_discrimination(behaviour_matrix)
    vis_performance = [vis_trial_outcome_list, vis_hits, vis_misses, vis_false_alarms, vis_correct_rejections]

    # Get Odour Discrimination
    odour_trial_outcome_list, odour_hits, odour_misses, odour_false_alarms, odour_correct_rejections = Behaviour_Analysis_Functions.analyse_odour_discrimination(behaviour_matrix)
    odour_performance = [odour_trial_outcome_list, odour_hits, odour_misses, odour_false_alarms, odour_correct_rejections]

    # Get Irrel Ignore
    irrel_responses = Behaviour_Analysis_Functions.analyse_irrelevant_performance(behaviour_matrix)
    irrel_percentage = float(irrel_responses.count(1)) / len(irrel_responses)

    # Get Perfect Transition Performance
    transition_outcome_list = Behaviour_Analysis_Functions.analyse_transition_proportions(behaviour_matrix)
    perfect_transitions = transition_outcome_list.count(1)
    missed_transitions = transition_outcome_list.count(0)
    if perfect_transitions + missed_transitions > 0:
        transition_percentages = float(perfect_transitions) / (perfect_transitions + missed_transitions)
    else:
        transition_percentages = np.nan
    return vis_performance, odour_performance, irrel_percentage, transition_percentages, transition_outcome_list



def perfom_transition_analysis(mouse_directory):

    # Load Transition Sessions
    behavioural_sessions = os.listdir(mouse_directory)
    transition_session_list = []
    for session in behavioural_sessions:
        if 'Transition' in session:
            transition_session_list.append(session)

    # Analyse Sessions
    visual_performance_list = []
    odour_performance_list = []
    irrel_performance_list = []
    transition_percentage_list = []
    transition_outcome_list = []

    for session in transition_session_list:
        print("Session: ", session)
        vis_performance, odour_performance, irrel_percentage, transition_percentages, transition_outcomes = analyse_transition_session(os.path.join(mouse_directory, session))
        visual_performance_list.append(vis_performance)
        odour_performance_list.append(odour_performance)
        irrel_performance_list.append(irrel_percentage)
        transition_percentage_list.append(transition_percentages)
        transition_outcome_list.append(transition_outcomes)

    return visual_performance_list, odour_performance_list, irrel_performance_list, transition_percentage_list, transition_outcome_list



def plot_discrimination_performance(group_performance_list, title=""):

    for mouse_list in group_performance_list:
        hit_cross_session_list = []

        for session in mouse_list:
            trial_outcome_list = session[0]
            hits = session[1]
            misses = session[2]
            false_alarms = session[3]
            correct_rejections = session[4]

            total_trials = hits + misses + false_alarms + correct_rejections
            correct_trials = hits + correct_rejections
            percentage_correct = float(correct_trials) / total_trials

            hit_cross_session_list.append(percentage_correct)

        plt.plot(hit_cross_session_list)

    plt.title(title)
    plt.ylim([0, 1])
    plt.show()

"""
def plot_irrel_performance(group_performance_list, title=""):

    for mouse_list in group_performance_list:
        session_performance_list = []

        for session_performance in mouse_list:
            session_performance_list.append(session_performance)


        plt.plot(session_performance_list)

    plt.title(title)
    plt.ylim([0, 1])
    plt.show()
"""

def remove_nans_from_list(original_list):

    new_list = []
    for item in original_list:
        if math.isnan(item) == False:
            new_list.append(item)
    return new_list


def plot_transition_performance(group_performance_list, title=""):

    for mouse_list in group_performance_list:
        session_performance_list = []

        for session_performance in mouse_list:
            session_performance_list.append(session_performance)


        plt.plot(session_performance_list)

    plt.title(title)
    plt.ylim([0, 1])
    plt.show()


def analyse_group(group_list):

    # Analyse Behaviour Matricies
    group_visual_performance_list = []
    group_odour_performance_list = []
    group_irrel_performance_list = []
    group_odour_to_visual_transition_performance_list = []
    group_visual_to_odour_transition_performance_list = []

    group_odour_to_visual_transition_distribution = []
    group_visual_to_odour_transition_distribution = []

    for mouse in group_list:

        mouse_visual_performance_list = []
        mouse_odour_performance_list = []
        mouse_irrel_performance_list = []
        mouse_transition_performance_list = []

        for session in mouse:

            # Analyse Performance
            [vis_performance, odour_performance, irrel_percentage, transition_percentages, transition_outcome_list, odour_to_visual_transition_distribution, visual_to_odour_transition_distribution] = Transition_Analysis.analyse_transition_session(session)
            #print("Session: ", session)
            #print("odour_to_visual_transition_distribution", odour_to_visual_transition_distribution)
            #plt.hist(transition_distribution)
            #plt.show()

            mouse_visual_performance_list.append(vis_performance)
            mouse_odour_performance_list.append(odour_performance)
            mouse_irrel_performance_list.append(irrel_percentage)
            mouse_transition_performance_list.append(transition_percentages)
            #print("visual_to_odour_transition_distribution", visual_to_odour_transition_distribution)


            for value in odour_to_visual_transition_distribution:
                group_odour_to_visual_transition_distribution.append(value)

            for value in visual_to_odour_transition_distribution:
                group_visual_to_odour_transition_distribution.append(value)

        group_irrel_performance_list.append(mouse_irrel_performance_list)

        #group_visual_performance_list.append(visual_performance_list)
        #group_odour_performance_list.append(odour_performance_list)
        #group_irrel_performance_list.append(irrel_performance_list)
        #group_transition_performance_list.append(transition_percentage_list)

    #plot_discrimination_performance(group_visual_performance_list, title="Visual Performance")
    #plot_discrimination_performance(group_odour_performance_list, title="Odour Performance")
    #plot_irrel_performance(group_irrel_performance_list, title="Irrelevant Performance")
    #plot_transition_performance(group_transition_performance_list, title="Transition Performance")

    #return group_visual_performance_list, group_odour_performance_list, group_irrel_performance_list, group_irrel_performance_list


    return [group_odour_to_visual_transition_distribution, group_visual_to_odour_transition_distribution, group_irrel_performance_list]


def plot_transition_trials_histogram(control_transition_distribution, mutant_transition_distribution):

    # Get Bins
    control_transition_distribution_set = set(control_transition_distribution)
    mutant_transition_distribution_set = set(mutant_transition_distribution)
    control_transition_distribution_set = remove_nans_from_list(control_transition_distribution_set)
    mutant_transition_distribution_set = remove_nans_from_list(mutant_transition_distribution_set)
    control_bins = list(range(int(np.max(control_transition_distribution_set))))
    mutant_bins = list(range(int(np.max(mutant_transition_distribution_set))))

    # Get X Ticks
    x_ticks = list(range(int(np.max(control_bins + mutant_bins))))

    # Plot Data
    plt.title("Transition Trials Distribution")
    plt.hist(control_transition_distribution, bins=control_bins, color='b', alpha=0.5, density=True)
    plt.hist(mutant_transition_distribution, bins=mutant_bins, color='g', alpha=0.5, density=True)
    plt.xticks(x_ticks)
    plt.ylabel("Count")
    plt.xlabel("Missed Rewarded Visual Gratings")

    # Add Legends
    blue_patch = mpatches.Patch(color='blue', label='Controls')
    green_patch = mpatches.Patch(color='green', label='Mutants')
    ax = plt.gca()
    ax.legend(handles=[blue_patch, green_patch])

    plt.show()


def plot_irrel_performance(control_group_irrel_performance_list, mutant_group_irrel_performance_list):


    # Create Dataframe
    combined_performance_list = []
    combined_mouse_name_list = []

    mouse_count = 0

    mouse_names = ["a", "b", "c", "d", "e"]
    for mouse_session_list in group_irrel_performance_list:

        for value in mouse_session_list:
            combined_performance_list.append(value)
            combined_mouse_name_list.append(mouse_names[mouse_count])

        mouse_count += 1


    dataframe = pd.DataFrame()
    dataframe["Irrel Performance"] = combined_performance_list
    dataframe["Mouse"] = combined_mouse_name_list

    print("Irrel Performance", combined_performance_list)
    print("Mouse indexes", combined_mouse_name_list)
    #seaborn.swarmplot(y="Irrel Performance", orient='v', hue="Mouse", data=dataframe)
    seaborn.swarmplot(y = dataframe["Irrel Performance"], hue = dataframe["Mouse"], x = [""] * len(dataframe))
    plt.show()




control_session_list = [

    # 4.1B
    [
        r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Controls/4.1B/2021_04_02_Transition_Imaging",
        #r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Controls/4.1B/2021_04_04_Transition_Imaging",
        r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Controls/4.1B/2021_04_05_Transition_Behaviour",
        r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Controls/4.1B/2021_04_08_Transition_Imaging",
        r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Controls/4.1B/2021_04_09_Transition_Behaviour",
        r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Controls/4.1B/2021_04_10_Transition_Imaging"
    ],

    # 7.1B
    [
        r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Controls/7.1B/2021_03_22_Transition_Behaviour",
        r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Controls/7.1B/2021_03_23_Transition_Imaging",
        r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Controls/7.1B/2021_03_24_Transition_Behaviour",
        r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Controls/7.1B/2021_03_27_Transition_Imaging",
        r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Controls/7.1B/2021_03_30_Transition_Behaviour",
        r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Controls/7.1B/2021_03_31_Transition_Imaging",
        r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Controls/7.1B/2021_04_01_Transition_Behaviour",
        r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Controls/7.1B/2021_04_02_Transition_Imaging",
    ],

    # 14.1A
    [
        r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Controls/14.1A/2021_06_12_Transition_Behaviour",
        r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Controls/14.1A/2021_06_13_Transition_Imaging",
        r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Controls/14.1A/2021_06_14_Transition_Behaviour",
        r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Controls/14.1A/2021_06_15_Transition_Imaging",
        r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Controls/14.1A/2021_06_16_Transition_Behaviour",
        r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Controls/14.1A/2021_06_17_Transition_Behaviour",
    ],

    # 22.1A
    [
        r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Controls/22.1A/2021_10_26_Transition_Imaging",
        r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Controls/22.1A/2021_10_29_Transition_Imaging",
        r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Controls/22.1A/2021_11_02_Transition_Behaviour",
        r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Controls/22.1A/2021_11_03_Transition_Imaging",
        r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Controls/22.1A/2021_11_04_Transition_Behaviour",
        r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Controls/22.1A/2021_11_05_Transition_Imaging",
    ],
]




mutant_session_list = [

    [
        r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Mutants/4.1A/2021_04_08_Transition_Imaging",
        r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Mutants/4.1A/2021_04_10_Transition_Imaging",
        r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Mutants/4.1A/2021_04_11_Transition_Behaviour",
        r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Mutants/4.1A/2021_04_12_Transition_Imaging",
    ],


    [
        r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Mutants/10.1A/2021_06_13_Transition_Behaviour",
        r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Mutants/10.1A/2021_06_14_Transition_Imaging",
        r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Mutants/10.1A/2021_06_16_Transition_Imaging",
        r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Mutants/10.1A/2021_06_17_Transition_Behaviour",
        r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Mutants/10.1A/2021_06_18_Transition_Imaging",
    ],


    [
        r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Mutants/20.1B/2021_11_22_Transition_Imaging",
        r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Mutants/20.1B/2021_11_23_Transition_Behaviour",
        r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Mutants/20.1B/2021_11_24_Transition_Imaging",
        r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Mutants/20.1B/2021_11_26_Transition_Imaging",
    ],

    [
        r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Mutants/24.1C/2021_11_05_Transition_Imaging",
        r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Mutants/24.1C/2021_11_08_Transition_Imaging",
        r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Mutants/24.1C/2021_11_10_Transition_Imaging",
    ]
]



[control_odour_to_visual_transition_distribution,
 control_visual_to_odour_transition_distribution,
 control_irrel_performance_list] = analyse_group(control_session_list)

print("Control Irrel Performane List", control_irrel_performance_list)

plot_irrel_performance(control_irrel_performance_list)

[mutant_odour_to_visual_transition_distribution,
 mutant_visual_to_odour_transition_distribution,
 mutant_irrel_performance_list] = analyse_group(mutant_session_list)



print("Mutant Irrel Performane List", mutant_irrel_performance_list)

plot_transition_trials_histogram(control_odour_to_visual_transition_distribution, mutant_odour_to_visual_transition_distribution)
plot_transition_trials_histogram(control_visual_to_odour_transition_distribution, mutant_visual_to_odour_transition_distribution)


