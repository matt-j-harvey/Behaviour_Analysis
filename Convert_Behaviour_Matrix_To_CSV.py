import numpy as np
import os

def save_behaviour_matrix_as_svd(behaviour_matrix, save_directory):

    header = [
        "0 trial_index," 
        "1 trial_type,"
        "2 lick,"
        "3 correct,"
        "4 rewarded,"
        "5 preeceded_by_irrel,"
        "6 irrel_type,"
        "7 ignore_irrel,"
        "8 block_number,"
        "9 first_in_block,"
        "10 in_block_of_stable_performance,"
        "11 stimuli_onset,"
        "12 stimuli_offset,"
        "13 irrel_onset,"
        "14 irrel_offset,"
        "15 trial_end,"
        "16 Photodiode Onset,"
        "17 Photodiode Offset,"
        ]
    header = " ".join(header)

    np.savetxt(os.path.join(save_directory, "Behaviour_Matrix.csv"), behaviour_matrix, delimiter=",", fmt="%.2f",
               header=header, comments="")


base_directory = r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Controls/4.1B/2021_04_10_Transition_Imaging"
behaviour_matrix = np.load(os.path.join(base_directory, "Stimuli_Onsets", "Behaviour_Matrix.npy"), allow_pickle=True)
save_behaviour_matrix_as_svd(behaviour_matrix, base_directory)