import os

import numpy as np
import sys
import matplotlib.pyplot as plt

import Create_Behaviour_Matrix
import Behaviour_Analysis_Functions




def create_behaviour_matricies(mouse_directory, lick_threshold):

    # Load Transition Sessions
    behavioural_sessions = os.listdir(mouse_directory)
    transition_session_list = []
    for session in behavioural_sessions:
        if 'Transition' in session:
            transition_session_list.append(session)

    for session in transition_session_list:
        Create_Behaviour_Matrix.create_behaviour_matrix(os.path.join(mouse_directory, session), lick_threshold=lick_threshold, behaviour_only=True)



def check_if_transitioned(behaviour_matrix, count_start):

    index_1 = count_start + 0
    index_2 = count_start + 1
    index_3 = count_start + 2

    # Check There are still 3 Trials Left
    number_of_trials = np.shape(behaviour_matrix)[0]
    if index_3 >= number_of_trials:
        return "Error"

    # Check All 3 Are Rewarded Visuals
    if behaviour_matrix[index_1][1] == 1 and behaviour_matrix[index_2][1] == 1 and behaviour_matrix[index_3][1] == 1:
        if behaviour_matrix[index_1][3] == 1 and behaviour_matrix[index_2][3] == 1 and behaviour_matrix[index_3][3] == 1:
            return True
        else:
            return False
    else:
        return "Error"




def check_if_transitioned_visual_to_odour(behaviour_matrix, count_start):

    index_1 = count_start + 0
    index_2 = count_start + 1
    index_3 = count_start + 2

    # Check There are still 3 Trials Left
    number_of_trials = np.shape(behaviour_matrix)[0]
    if index_3 >= number_of_trials:
        return "Error"

    # Check All 3 Are Preceeded By Rewarded Visuals
    if behaviour_matrix[index_1][6] == 1 and behaviour_matrix[index_2][6] == 1 and behaviour_matrix[index_3][6] == 1:

        # Check All 3 Have Ignored Lick
        if behaviour_matrix[index_1][7] == 1 and behaviour_matrix[index_2][7] == 1 and behaviour_matrix[index_3][7] == 1:
            return True
        else:
            return False
    else:
        return "Error"




def get_transition_distribution(behaviour_matrix):

    # Get Transition Trials
    transition_trial_list = []
    number_of_trials = np.shape(behaviour_matrix)[0]
    for trial_index in range(number_of_trials):
        if behaviour_matrix[trial_index][1] == 1 and behaviour_matrix[trial_index][9] == 1:
            transition_trial_list.append(trial_index)

    # For Each Transition Trial
    transition_distribution = []
    for transition_trial in transition_trial_list:

        missed_vis_1_count = 0
        has_transitioned = False
        while has_transitioned == False:
                has_transitioned = check_if_transitioned(behaviour_matrix, transition_trial + missed_vis_1_count)

                if has_transitioned == True:
                    transition_distribution.append(missed_vis_1_count)

                elif has_transitioned == False:
                    missed_vis_1_count += 1

                elif has_transitioned == "Error":
                    transition_distribution.append(np.nan)
                    break


    return transition_distribution




def get_visual_to_odour_transition_distribution(behaviour_matrix):

    # Get Transition Trials
    # First Trial In Block + Rewarded Odour
    transition_trial_list = []
    number_of_trials = np.shape(behaviour_matrix)[0]
    for trial_index in range(number_of_trials):
        if behaviour_matrix[trial_index][1] == 3 and behaviour_matrix[trial_index][9] == 1:
            transition_trial_list.append(trial_index)

    # For Each Transition Trial
    transition_distribution = []
    for transition_trial in transition_trial_list:

        lick_to_irrel_vis_1_count = 0
        has_transitioned = False
        while has_transitioned == False:
                has_transitioned = check_if_transitioned_visual_to_odour(behaviour_matrix, transition_trial + lick_to_irrel_vis_1_count)

                if has_transitioned == True:
                    transition_distribution.append(lick_to_irrel_vis_1_count)

                elif has_transitioned == False:
                    lick_to_irrel_vis_1_count += 1

                elif has_transitioned == "Error":
                    transition_distribution.append(np.nan)
                    break


    return transition_distribution



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

    # Get Transition Distributions
    transition_distribution = get_transition_distribution(behaviour_matrix)

    # Get Visual To Odour Distribution
    visual_to_odour_transition_distribution = get_visual_to_odour_transition_distribution(behaviour_matrix)

    return [vis_performance, odour_performance, irrel_percentage, transition_percentages, transition_outcome_list, transition_distribution, visual_to_odour_transition_distribution]



def perform_transition_analysis(mouse_directory):

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


def plot_irrel_performance(group_performance_list, title=""):

    for mouse_list in group_performance_list:
        session_performance_list = []

        for session_performance in mouse_list:
            session_performance_list.append(session_performance)


        plt.plot(session_performance_list)

    plt.title(title)
    plt.ylim([0, 1])
    plt.show()



def plot_transition_performance(group_performance_list, title=""):

    for mouse_list in group_performance_list:
        session_performance_list = []

        for session_performance in mouse_list:
            session_performance_list.append(session_performance)


        plt.plot(session_performance_list)

    plt.title(title)
    plt.ylim([0, 1])
    plt.show()
