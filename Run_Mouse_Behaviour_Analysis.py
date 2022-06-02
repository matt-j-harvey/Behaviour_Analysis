import os
import Create_Behaviour_Matrix
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

"""
Controls: 
78.1A
78.1D
7.1B
4.1B
14.1A
22.1A


Mutants:
71.2A
4.1A
10.1A
16.1B
24.1C
20.1B
"""


session_directory = "/media/matthew/29D46574463D2856/Behaviour_Analysis/Controls/14.1A"
session_directory = "/media/matthew/29D46574463D2856/Behaviour_Analysis/Controls/22.1A"
session_directory = "/media/matthew/29D46574463D2856/Behaviour_Analysis/Controls/7.1B"
session_directory = "/media/matthew/29D46574463D2856/Behaviour_Analysis/Controls/4.1B"

# Mutants
session_directory = "/media/matthew/29D46574463D2856/Behaviour_Analysis/Mutants/20.1B"



session_list = os.listdir(session_directory)


for base_directory in session_list:
    Create_Behaviour_Matrix.create_behaviour_matrix(os.path.join(session_directory, base_directory), lick_threshold=0.1, behaviour_only=True)






"""
visual_performance_list = []
odour_performance_list = []
irrel_performance_list = []

for base_directory in session_list:
    #Create_Behaviour_Matrix.create_behaviour_matrix(os.path.join(session_directory, base_directory), lick_threshold=0.4, behaviour_only=True)

    behaviour_matrix = np.load(os.path.join(session_directory, base_directory, "Stimuli_Onsets", "Behaviour_Matrix.npy"), allow_pickle=True)

    trial_outcome_list, hits, misses, false_alarms, correct_rejections = analyse_visual_discrimination(behaviour_matrix)
    visual_performance = np.mean(trial_outcome_list)

    trial_outcome_list, hits, misses, false_alarms, correct_rejections = analyse_odour_discrimination(behaviour_matrix)
    odour_performance = np.mean(trial_outcome_list)

    irrel_responses = analyse_irrelevant_performance(behaviour_matrix)
    irrel_performance = np.mean(irrel_responses)
    print(irrel_performance)

    visual_performance_list.append(visual_performance)
    odour_performance_list.append(odour_performance)
    irrel_performance_list.append(irrel_performance)


plt.plot(odour_performance_list, c='g')
plt.plot(visual_performance_list, c='b')
plt.plot(irrel_performance_list, c='m')
plt.ylim([0.5, 1])
plt.show()

"""


# Things To Record
# Visual Discrimination
# Odour Discrimination
# Irrel Lick Rate