import numpy as np
import matplotlib.pyplot as plt
import os
from matplotlib.gridspec import GridSpec

def get_session_reaction_times(behaviour_matrix):

    vis_1_reaction_times = []
    vis_2_reaction_times = []

    for trial in behaviour_matrix:
        stimuli_onset = trial[11]
        lick = trial[2]
        trial_type = trial[1]
        lick_onset = trial[18]
        correct = trial[3]

        if lick == 1:
            print("Lick Onset", lick_onset)
            print("Stimuli Onset", stimuli_onset)
            reaction_time = lick_onset - stimuli_onset

            if trial_type == 1:
                if correct == 1:
                    if reaction_time < 4000:
                        vis_1_reaction_times.append(reaction_time)

            elif trial_type == 2:
                if correct == 0:
                    vis_2_reaction_times.append(reaction_time)

    return vis_1_reaction_times, vis_2_reaction_times



def get_mouse_reaction_times(mouse_session_list):

    vis_1_mean_reaction_times = []
    vis_2_mean_reaction_times = []

    vis_1_reaction_times_meta_list = []
    vis_2_reaction_times_meta_list = []

    for session in mouse_session_list:

        # Load Behaviour Matrix
        behaviour_matrix = np.load(os.path.join(session, "Stimuli_Onsets", "Behaviour_Matrix.npy"), allow_pickle=True)

        vis_1_reaction_times, vis_2_reaction_times = get_session_reaction_times(behaviour_matrix)

        for time in vis_1_reaction_times:
            vis_1_reaction_times_meta_list.append(time)

        for time in vis_2_reaction_times:
            vis_2_reaction_times_meta_list.append(time)

        vis_1_mean = np.median(vis_1_reaction_times)
        vis_2_mean = np.median(vis_2_reaction_times)

        vis_1_mean_reaction_times.append(vis_1_mean)
        vis_2_mean_reaction_times.append(vis_2_mean)


    #plt.scatter(list(range(len(vis_1_reaction_times_meta_list))), vis_1_reaction_times_meta_list, alpha=0.5, c='b')
    #plt.scatter(list(range(len(vis_2_reaction_times_meta_list))), vis_2_reaction_times_meta_list, alpha=0.5, c='r')
    #plt.show()
    #plt.plot(vis_1_mean_reaction_times)
    #plt.plot(vis_2_mean_reaction_times)
    #plt.show()
    return vis_1_mean_reaction_times, vis_2_mean_reaction_times



def get_session_list_reaction_times(session_list):

    combined_vis_1_reaction_times = []
    combined_vis_2_reaction_times = []

    for session in session_list:

        # Load Behaviour Matrix
        behaviour_matrix = np.load(os.path.join(session, "Stimuli_Onsets", "Behaviour_Matrix.npy"), allow_pickle=True)

        vis_1_reaction_times, vis_2_reaction_times = get_session_reaction_times(behaviour_matrix)

        for reaction in vis_1_reaction_times:
            combined_vis_1_reaction_times.append(reaction)
        for reaction in vis_2_reaction_times:
            combined_vis_2_reaction_times.append(reaction)

    return combined_vis_1_reaction_times, combined_vis_2_reaction_times


def get_combine_list(sessions_dict):

    combined_list = []

    mice_nams = list(sessions_dict.keys())
    for mouse in mice_nams:
        mouse_sessions = sessions_dict[mouse]
        for session in mouse_sessions:
            combined_list.append(session)

    return combined_list




def split_sessions_By_d_prime(session_list, intermediate_threshold, post_threshold):

    pre_learning_sessions = []
    intermediate_learning_sessions = []
    post_learning_sessions = []

    # Iterate Throug Sessions
    for session in session_list:

        # Load D Prime
        behavioural_dictionary = np.load(os.path.join(session, "Behavioural_Measures", "Performance_Dictionary.npy"), allow_pickle=True)[()]
        d_prime = behavioural_dictionary["visual_d_prime"]

        if d_prime >= post_threshold:
            post_learning_sessions.append(session)

        if d_prime < post_threshold and d_prime >= intermediate_threshold:
            intermediate_learning_sessions.append(session)

        if d_prime < intermediate_threshold:
            pre_learning_sessions.append(session)

    return pre_learning_sessions, intermediate_learning_sessions, post_learning_sessions


def get_reaction_time_distributions(session_list):

    intermeidate_threshold = 1
    post_threshold = 2

    pre_learning_sessions, intermediate_learning_sessions, post_learning_sessions = split_sessions_By_d_prime(session_list, intermeidate_threshold, post_threshold)

    pre_combined_vis_1_reaction_times, pre_combined_vis_2_reaction_times = get_session_list_reaction_times(pre_learning_sessions)
    int_combined_vis_1_reaction_times, int_combined_vis_2_reaction_times = get_session_list_reaction_times(intermediate_learning_sessions)
    post_combined_vis_1_reaction_times, post_combined_vis_2_reaction_times = get_session_list_reaction_times(post_learning_sessions)

    return [pre_combined_vis_1_reaction_times,
            pre_combined_vis_2_reaction_times,
            int_combined_vis_1_reaction_times,
            int_combined_vis_2_reaction_times,
            post_combined_vis_1_reaction_times,
            post_combined_vis_2_reaction_times,]

control_sessions = {

    "78.1A":[   r"/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NRXN78.1A/2020_11_15_Discrimination_Imaging",
                r"/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NRXN78.1A/2020_11_16_Discrimination_Imaging",
                r"/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NRXN78.1A/2020_11_17_Discrimination_Imaging",
                r"/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NRXN78.1A/2020_11_19_Discrimination_Imaging",
                r"/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NRXN78.1A/2020_11_21_Discrimination_Imaging",
                r"/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NRXN78.1A/2020_11_24_Discrimination_Imaging"],


    "78.1D":[   r"/media/matthew/Expansion/Widefield_Analysis/NRXN78.1D/2020_11_14_Discrimination_Imaging",
                r"/media/matthew/Expansion/Widefield_Analysis/NRXN78.1D/2020_11_15_Discrimination_Imaging",
                r"/media/matthew/Expansion/Widefield_Analysis/NRXN78.1D/2020_11_16_Discrimination_Imaging",
                r"/media/matthew/Expansion/Widefield_Analysis/NRXN78.1D/2020_11_17_Discrimination_Imaging",
                r"/media/matthew/Expansion/Widefield_Analysis/NRXN78.1D/2020_11_19_Discrimination_Imaging",
                r"/media/matthew/Expansion/Widefield_Analysis/NRXN78.1D/2020_11_21_Discrimination_Imaging",
                r"/media/matthew/Expansion/Widefield_Analysis/NRXN78.1D/2020_11_23_Discrimination_Imaging",
                r"/media/matthew/Expansion/Widefield_Analysis/NRXN78.1D/2020_11_25_Discrimination_Imaging"],


    "4.1B":[    r"/media/matthew/Expansion/Widefield_Analysis/NXAK4.1B/2021_02_04_Discrimination_Imaging",
                r"/media/matthew/Expansion/Widefield_Analysis/NXAK4.1B/2021_02_06_Discrimination_Imaging",
                r"/media/matthew/Expansion/Widefield_Analysis/NXAK4.1B/2021_02_08_Discrimination_Imaging",
                r"/media/matthew/Expansion/Widefield_Analysis/NXAK4.1B/2021_02_10_Discrimination_Imaging",
                r"/media/matthew/Expansion/Widefield_Analysis/NXAK4.1B/2021_02_12_Discrimination_Imaging",
                r"/media/matthew/Expansion/Widefield_Analysis/NXAK4.1B/2021_02_14_Discrimination_Imaging",
                r"/media/matthew/Expansion/Widefield_Analysis/NXAK4.1B/2021_02_22_Discrimination_Imaging"],


    "22.1":[    r"/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NXAK22.1A/2021_09_25_Discrimination_Imaging",
                r"/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NXAK22.1A/2021_09_29_Discrimination_Imaging",
                r"/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NXAK22.1A/2021_10_01_Discrimination_Imaging",
                r"/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NXAK22.1A/2021_10_03_Discrimination_Imaging",
                r"/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NXAK22.1A/2021_10_05_Discrimination_Imaging",
                r"/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NXAK22.1A/2021_10_07_Discrimination_Imaging",
                r"/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NXAK22.1A/2021_10_08_Discrimination_Imaging"],


    # 14.1A - 6
    "14.1A": [  r"/media/matthew/Expansion/Widefield_Analysis/NXAK14.1A/2021_04_29_Discrimination_Imaging",
                r"/media/matthew/Expansion/Widefield_Analysis/NXAK14.1A/2021_05_01_Discrimination_Imaging",
                r"/media/matthew/Expansion/Widefield_Analysis/NXAK14.1A/2021_05_03_Discrimination_Imaging",
                r"/media/matthew/Expansion/Widefield_Analysis/NXAK14.1A/2021_05_05_Discrimination_Imaging",
                r"/media/matthew/Expansion/Widefield_Analysis/NXAK14.1A/2021_05_07_Discrimination_Imaging",
                r"/media/matthew/Expansion/Widefield_Analysis/NXAK14.1A/2021_05_09_Discrimination_Imaging"],

    "7.1B": [   r"/media/matthew/Expansion/Widefield_Analysis/NXAK7.1B/2021_02_01_Discrimination_Imaging",
                r"/media/matthew/Expansion/Widefield_Analysis/NXAK7.1B/2021_02_03_Discrimination_Imaging",
                r"/media/matthew/Expansion/Widefield_Analysis/NXAK7.1B/2021_02_05_Discrimination_Imaging",
                r"/media/matthew/Expansion/Widefield_Analysis/NXAK7.1B/2021_02_07_Discrimination_Imaging",
                r"/media/matthew/Expansion/Widefield_Analysis/NXAK7.1B/2021_02_09_Discrimination_Imaging",
                r"/media/matthew/Expansion/Widefield_Analysis/NXAK7.1B/2021_02_11_Discrimination_Imaging",
                r"/media/matthew/Expansion/Widefield_Analysis/NXAK7.1B/2021_02_13_Discrimination_Imaging",
                r"/media/matthew/Expansion/Widefield_Analysis/NXAK7.1B/2021_02_15_Discrimination_Imaging",
                r"/media/matthew/Expansion/Widefield_Analysis/NXAK7.1B/2021_02_17_Discrimination_Imaging",
                r"/media/matthew/Expansion/Widefield_Analysis/NXAK7.1B/2021_02_19_Discrimination_Imaging",
                r"/media/matthew/Expansion/Widefield_Analysis/NXAK7.1B/2021_02_22_Discrimination_Imaging",
                r"/media/matthew/Expansion/Widefield_Analysis/NXAK7.1B/2021_02_24_Discrimination_Imaging"],
    }


mutant_sessions = {

    "4.1A":[r"/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NXAK4.1A/2021_02_02_Discrimination_Imaging",
            r"/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NXAK4.1A/2021_02_04_Discrimination_Imaging",
            r"/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NXAK4.1A/2021_02_06_Discrimination_Imaging",
            r"/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NXAK4.1A/2021_02_08_Discrimination_Imaging",
            r"/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NXAK4.1A/2021_02_10_Discrimination_Imaging",
            r"/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NXAK4.1A/2021_02_12_Discrimination_Imaging",
            r"/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NXAK4.1A/2021_02_14_Discrimination_Imaging",
            r"/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NXAK4.1A/2021_02_16_Discrimination_Imaging",
            r"/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NXAK4.1A/2021_02_18_Discrimination_Imaging",
            r"/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NXAK4.1A/2021_02_23_Discrimination_Imaging",
            r"/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NXAK4.1A/2021_02_25_Discrimination_Imaging",
            r"/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NXAK4.1A/2021_02_27_Discrimination_Imaging",
            r"/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NXAK4.1A/2021_03_01_Discrimination_Imaging",
            r"/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NXAK4.1A/2021_03_03_Discrimination_Imaging",
            r"/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NXAK4.1A/2021_03_05_Discrimination_Imaging",],

    "20.1B":[r"/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NXAK20.1B/2021_09_28_Discrimination_Imaging",
            r"/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NXAK20.1B/2021_09_30_Discrimination_Imaging",
            r"/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NXAK20.1B/2021_10_02_Discrimination_Imaging",
            r"/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NXAK20.1B/2021_10_04_Discrimination_Imaging",
            r"/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NXAK20.1B/2021_10_06_Discrimination_Imaging",
            r"/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NXAK20.1B/2021_10_09_Discrimination_Imaging",
            r"/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NXAK20.1B/2021_10_11_Discrimination_Imaging",
            r"/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NXAK20.1B/2021_10_13_Discrimination_Imaging",
            r"/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NXAK20.1B/2021_10_15_Discrimination_Imaging",
            r"/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NXAK20.1B/2021_10_17_Discrimination_Imaging",
            r"/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NXAK20.1B/2021_10_19_Discrimination_Imaging",],


    "24.1C":[r"/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NXAK24.1C/2021_09_20_Discrimination_Imaging",
            r"/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NXAK24.1C/2021_09_22_Discrimination_Imaging",
            r"/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NXAK24.1C/2021_09_24_Discrimination_Imaging",
            r"/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NXAK24.1C/2021_09_26_Discrimination_Imaging",
            r"/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NXAK24.1C/2021_09_28_Discrimination_Imaging",
            r"/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NXAK24.1C/2021_09_30_Discrimination_Imaging",
            r"/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NXAK24.1C/2021_10_02_Discrimination_Imaging",
            r"/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NXAK24.1C/2021_10_04_Discrimination_Imaging",
            r"/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NXAK24.1C/2021_10_06_Discrimination_Imaging",
            r"/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NXAK24.1C/2021_10_08_Discrimination_Imaging"],

    "16.1B":[r"/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NXAK16.1B/2021_04_30_Discrimination_Imaging",
            r"/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NXAK16.1B/2021_05_02_Discrimination_Imaging",
            r"/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NXAK16.1B/2021_05_04_Discrimination_Imaging",
            r"/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NXAK16.1B/2021_05_06_Discrimination_Imaging",
            r"/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NXAK16.1B/2021_05_08_Discrimination_Imaging",
            r"/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NXAK16.1B/2021_05_10_Discrimination_Imaging",
            r"/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NXAK16.1B/2021_05_12_Discrimination_Imaging",
            r"/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NXAK16.1B/2021_05_14_Discrimination_Imaging",
            r"/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NXAK16.1B/2021_05_16_Discrimination_Imaging",
            r"/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NXAK16.1B/2021_05_18_Discrimination_Imaging",
            r"/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NXAK16.1B/2021_05_20_Discrimination_Imaging",
            r"/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NXAK16.1B/2021_05_22_Discrimination_Imaging",
            r"/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NXAK16.1B/2021_05_24_Discrimination_Imaging",
            r"/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NXAK16.1B/2021_05_26_Discrimination_Imaging",
            r"/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NXAK16.1B/2021_06_04_Discrimination_Imaging",
            r"/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NXAK16.1B/2021_06_15_Discrimination_Imaging",],

    "10.1A":[r"/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NXAK10.1A/2021_04_30_Discrimination_Imaging",
            r"/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NXAK10.1A/2021_05_02_Discrimination_Imaging",
            r"/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NXAK10.1A/2021_05_04_Discrimination_Imaging",
            r"/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NXAK10.1A/2021_05_06_Discrimination_Imaging",
            r"/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NXAK10.1A/2021_05_08_Discrimination_Imaging",
            r"/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NXAK10.1A/2021_05_10_Discrimination_Imaging",
            r"/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NXAK10.1A/2021_05_12_Discrimination_Imaging",
            r"/media/matthew/Seagate Expansion Drive2/Processed_Widefield_Data/NXAK10.1A/2021_05_14_Discrimination_Imaging"]


    # 71.2A - 16
}





all_control_sessions = get_combine_list(control_sessions)
all_mutant_sessions = get_combine_list(mutant_sessions)



[
control_pre_combined_vis_1_reaction_times,
control_pre_combined_vis_2_reaction_times,
control_int_combined_vis_1_reaction_times,
control_int_combined_vis_2_reaction_times,
control_post_combined_vis_1_reaction_times,
control_post_combined_vis_2_reaction_times,] = get_reaction_time_distributions(all_control_sessions)


[
mutant_pre_combined_vis_1_reaction_times,
mutant_pre_combined_vis_2_reaction_times,
mutant_int_combined_vis_1_reaction_times,
mutant_int_combined_vis_2_reaction_times,
mutant_post_combined_vis_1_reaction_times,
mutant_post_combined_vis_2_reaction_times,] = get_reaction_time_distributions(all_mutant_sessions)


figure_1 = plt.figure()
gridspec_1 = GridSpec(2, 3, figure=figure_1)

vis_1_pre_learning_axis = figure_1.add_subplot(gridspec_1[0, 0])
vis_1_int_learning_axis = figure_1.add_subplot(gridspec_1[0, 1])
vis_1_post_learning_axis = figure_1.add_subplot(gridspec_1[0, 2])

vis_1_pre_learning_axis.set_title("Rewarded Pre Learning Reaction Times")
vis_1_int_learning_axis.set_title("Rewarded Intermediate Learning Reaction Times")
vis_1_post_learning_axis.set_title("Rewarded Post Learning Reaction Times")

vis_1_pre_learning_axis.hist(control_pre_combined_vis_1_reaction_times, alpha=0.5, color='b', density=True)
vis_1_int_learning_axis.hist(control_int_combined_vis_1_reaction_times, alpha=0.5, color='b', density=True)
vis_1_post_learning_axis.hist(control_post_combined_vis_1_reaction_times, alpha=0.5, color='b', density=True)

vis_1_pre_learning_axis.hist(mutant_pre_combined_vis_1_reaction_times, alpha=0.5, color='g', density=True)
vis_1_int_learning_axis.hist(mutant_int_combined_vis_1_reaction_times, alpha=0.5, color='g', density=True)
vis_1_post_learning_axis.hist(mutant_post_combined_vis_1_reaction_times, alpha=0.5, color='g', density=True)



vis_2_pre_learning_axis = figure_1.add_subplot(gridspec_1[1, 0])
vis_2_int_learning_axis = figure_1.add_subplot(gridspec_1[1, 1])
vis_2_post_learning_axis = figure_1.add_subplot(gridspec_1[1, 2])

vis_2_pre_learning_axis.set_title("Unrewarded Pre Learning Reaction Times")
vis_2_int_learning_axis.set_title("Unrewarded Intermediate Learning Reaction Times")
vis_2_post_learning_axis.set_title("Unrewarded Post Learning Reaction Times")

vis_2_pre_learning_axis.hist(control_pre_combined_vis_2_reaction_times, alpha=0.5, color='b', density=True)
vis_2_int_learning_axis.hist(control_int_combined_vis_2_reaction_times, alpha=0.5, color='b', density=True)
vis_2_post_learning_axis.hist(control_post_combined_vis_2_reaction_times, alpha=0.5, color='b', density=True)

vis_2_pre_learning_axis.hist(mutant_pre_combined_vis_2_reaction_times, alpha=0.5, color='g', density=True)
vis_2_int_learning_axis.hist(mutant_int_combined_vis_2_reaction_times, alpha=0.5, color='g', density=True)
vis_2_post_learning_axis.hist(mutant_post_combined_vis_2_reaction_times, alpha=0.5, color='g', density=True)


# Set Axes Labels
vis_2_pre_learning_axis.set_xlabel("Time (ms)")
vis_1_int_learning_axis.set_xlabel("Time (ms)")
vis_1_post_learning_axis.set_xlabel("Time (ms)")
vis_2_pre_learning_axis.set_xlabel("Time (ms)")
vis_2_int_learning_axis.set_xlabel("Time (ms)")
vis_2_post_learning_axis.set_xlabel("Time (ms)")

vis_2_pre_learning_axis.set_ylabel("Fraction")
vis_1_int_learning_axis.set_ylabel("Fraction")
vis_1_post_learning_axis.set_ylabel("Fraction")
vis_2_pre_learning_axis.set_ylabel("Fraction")
vis_2_int_learning_axis.set_ylabel("Fraction")
vis_2_post_learning_axis.set_ylabel("Fraction")

plt.show()


control_mice = list(control_sessions.keys())
for mouse in control_mice:
    vis_1_mean_reaction_times, vis_2_mean_reaction_times = get_mouse_reaction_times(control_sessions[mouse])

    plt.plot(vis_1_mean_reaction_times, c='b')
    #plt.plot(vis_2_mean_reaction_times, c='b')


print("Mutants: ")
mutant_mice = list(mutant_sessions.keys())
for mouse in mutant_mice:
    vis_1_mean_reaction_times, vis_2_mean_reaction_times = get_mouse_reaction_times(mutant_sessions[mouse])

    plt.plot(vis_1_mean_reaction_times, c='g')
    #plt.plot(vis_2_mean_reaction_times, c='g')
plt.show()


