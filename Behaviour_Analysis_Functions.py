import os
import numpy as np
import matplotlib.pyplot as plt


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

def analyse_visual_discrimination(behaviour_matrix):

    false_alarms = 0
    correct_rejections = 0
    hits = 0
    misses = 0
    trial_outcome_list = []

    # Get Matrix Strucutre
    number_of_trials = np.shape(behaviour_matrix)[0]

    for trial_index in range(number_of_trials):
        trial_data = behaviour_matrix[trial_index]

        trial_type = trial_data[1]

        # Get Outcome
        if trial_type == 1 or trial_type == 2:
            trial_outcome = trial_data[3]
            trial_outcome_list.append(trial_outcome)

        # Get Response
        lick = trial_data[2]

        # Rewarded Visual
        if trial_type == 1:
            if lick == 1:
                hits += 1
            elif lick == 0:
                misses += 1

        elif trial_type == 2:
            if lick == 1:
                false_alarms += 1
            elif lick == 0:
                correct_rejections += 1

    return trial_outcome_list, hits, misses, false_alarms, correct_rejections



def analyse_odour_discrimination(behaviour_matrix):

    false_alarms = 0
    correct_rejections = 0
    hits = 0
    misses = 0
    trial_outcome_list = []

    # Get Matrix Strucutre
    number_of_trials = np.shape(behaviour_matrix)[0]

    for trial_index in range(number_of_trials):
        trial_data = behaviour_matrix[trial_index]

        trial_type = trial_data[1]

        # Get Outcome
        if trial_type == 3 or trial_type == 4:
            trial_outcome = trial_data[3]
            trial_outcome_list.append(trial_outcome)

        # Get Response
        lick = trial_data[2]

        # Rewarded Visual
        if trial_type == 3:
            if lick == 1:
                hits += 1
            elif lick == 0:
                misses += 1

        elif trial_type == 4:
            if lick == 1:
                false_alarms += 1
            elif lick == 0:
                correct_rejections += 1

    return trial_outcome_list, hits, misses, false_alarms, correct_rejections


def analyse_irrelevant_performance(behaviour_matrix):

    # Get Matrix Strucutre
    number_of_trials = np.shape(behaviour_matrix)[0]

    irrel_responses = []

    for trial_index in range(number_of_trials):

        trial_data = behaviour_matrix[trial_index]
        trial_type = trial_data[1]

        if trial_type == 3 or trial_type == 4:
            preceeded_by_irrel = trial_data[5]

            if preceeded_by_irrel == 1:
                ignore_irrel = trial_data[7]

                irrel_responses.append(ignore_irrel)

    return irrel_responses


def get_outcome_of_next_n_trials(behaviour_matrix, trial_index, n=3):

    number_of_trials = np.shape(behaviour_matrix)[0]
    outcome_list = []

    for x in range(1, n+1):
        selected_trial = trial_index + x

        if selected_trial >= number_of_trials:
            return False

        else:
            trial_outcome = behaviour_matrix[selected_trial][3]
            outcome_list.append(trial_outcome)

    if np.sum(outcome_list) == n:
        return True
    else:
        return False




def analyse_transition_proportions(behaviour_matrix):

    transition_outcome_list = []
    # 1 for Perfect transition
    # 0 for Missed transition
    # -1 for Fluke

    # Get Matrix Structure
    number_of_trials = np.shape(behaviour_matrix)[0]

    for trial_index in range(number_of_trials):
        trial_data = behaviour_matrix[trial_index]

        # Check Is First in Block
        first_in_block = trial_data[9]

        # Check Is Vis 1
        trial_type = trial_data[1]

        # If Visual Block VIs 1 and First In BLock
        if trial_type == 1 and first_in_block == 1:

            # Trial Outcome
            trial_outcome = trial_data[3]

            # If Mouse Didnt Lick To IT
            if trial_outcome == 0:

                # Get Outcome Of Next N Trials
                outcome_of_next_n_trials = get_outcome_of_next_n_trials(behaviour_matrix, trial_index)

                # But Mouse Did Lick To Next 3 Trials
                if outcome_of_next_n_trials == True:

                    # Its A Perfect Switch
                    transition_outcome = 1

                # Otherwise Its a Missed Switch
                else:
                    transition_outcome = 0

            # If Mouse Did Lick To It, Its a Fluke
            else:
                transition_outcome = -1


            transition_outcome_list.append(transition_outcome)

    return transition_outcome_list
