import os
import Behaviour_Analysis_Functions
import numpy as np

def analyse_transition_session(base_directory):

    # Load Behaviour Matrix
    behaviour_matrix = np.load(os.path.join(base_directory, "Stimuli_Onsets", "Behaviour_Matrix.npy"), allow_pickle=True)
    
    # Create Output Directory
    output_directory = os.path.join(base_directory, "Behavioural_Measures")
    if not os.path.exists(output_directory):
        os.mkdir(output_directory)

    # Average Visual Performance
    visual_trial_outcome_list, visual_hits, visual_misses, visual_false_alarms, visual_correct_rejections, visual_d_prime = Behaviour_Analysis_Functions.analyse_visual_discrimination(behaviour_matrix)
  
    # Average Odour Performance
    odour_trial_outcome_list, odour_hits, odour_misses, odour_false_alarms, odour_correct_rejections, odour_d_prime = Behaviour_Analysis_Functions.analyse_odour_discrimination(behaviour_matrix)

    # Odour To Visual Transition Distribution
    odour_to_visual_transition_distribution = Behaviour_Analysis_Functions.get_odour_to_visual_transition_distribution(behaviour_matrix)

    # Visual To Odour Transition Distribution
    visual_to_odour_transition_distribution = Behaviour_Analysis_Functions.get_visual_to_odour_transition_distribution(behaviour_matrix)

    # Average Visual Performance After Switching
    [visual_post_transition_trial_outcome_list,
     visual_post_transition_hits,
     visual_post_transition_misses,
     visual_post_transition_false_alarms,
     visual_post_transition_correct_rejections,
     visual_post_transition_visual_d_prime,
     visual_post_transition_trials_to_exclude] = Behaviour_Analysis_Functions.analyse_visual_performance_excluding_transitions(behaviour_matrix)

    # Blockwise D'Prime
    blockwise_visual_d_prime, blockwise_odour_d_prime = Behaviour_Analysis_Functions.calculate_blockwise_d_prime(behaviour_matrix)

    # Pack All This Into A Dictionary
    performance_dictionary = {

    "visual_trial_outcome_list.npy":visual_trial_outcome_list,
    "visual_hits.npy":visual_hits,
    "visual_misses.npy":visual_misses,
    "visual_false_alarms.npy":visual_false_alarms,
    "visual_correct_rejections":visual_correct_rejections,
    "visual_d_prime":visual_d_prime,

    "odour_trial_outcome_list.npy":odour_trial_outcome_list,
    "odour_hits.npy":odour_hits,
    "odour_misses.npy":odour_misses,
    "odour_false_alarms.npy":odour_false_alarms,
    "odour_correct_rejections":odour_correct_rejections,
    "odour_d_prime":odour_d_prime,

    "odour_to_visual_transition_distribution":odour_to_visual_transition_distribution,
    "visual_to_odour_transition_distribution":visual_to_odour_transition_distribution,

    "visual_post_transition_trial_outcome_list":visual_post_transition_trial_outcome_list,
    "visual_post_transition_hits":visual_post_transition_hits,
    "visual_post_transition_misses":visual_post_transition_misses,
    "visual_post_transition_false_alarms":visual_post_transition_false_alarms,
    "visual_post_transition_correct_rejections":visual_post_transition_correct_rejections,
    "visual_post_transition_visual_d_prime":visual_post_transition_visual_d_prime,
    "visual_post_transition_trials_to_exclude":visual_post_transition_trials_to_exclude,

    "blockwise_visual_d_prime":blockwise_visual_d_prime,
    "blockwise_odour_d_prime":blockwise_odour_d_prime

    }

    np.save(os.path.join(output_directory, "Performance_Dictionary.npy"), performance_dictionary)


session_list = [
    r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Controls/4.1B/2021_04_02_Transition_Imaging",
    r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Controls/4.1B/2021_04_05_Transition_Behaviour",
    r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Controls/4.1B/2021_04_08_Transition_Imaging",
    r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Controls/4.1B/2021_04_09_Transition_Behaviour",
    r"/media/matthew/Seagate Expansion Drive2/1TB Contents/Behaviour_Analysis/Controls/4.1B/2021_04_10_Transition_Imaging"
]

for session in session_list:
    analyse_transition_session(session)

