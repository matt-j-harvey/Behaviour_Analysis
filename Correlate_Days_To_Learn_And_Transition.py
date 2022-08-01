import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.stats import pearsonr


def create_session_list(base_directory):

    sub_directories = os.listdir(base_directory)

    session_list = []

    for directory in sub_directories:
        if "Switching" in directory or "Transition" in directory:
            session_list.append(os.path.join(base_directory,directory))

    return session_list


def create_transition_session_list(base_directory):

    sub_directories = os.listdir(base_directory)

    session_list = []

    for directory in sub_directories:
        if "Transition" in directory:
            session_list.append(os.path.join(base_directory,directory))

    return session_list



def clean_transition_distribution(transition_distribution):
    transition_distribution = np.nan_to_num(transition_distribution)

    clean_distribution = []

    for value in transition_distribution:
        if value != 0:
            clean_distribution.append(value)

    return clean_distribution


control_session_list = {

    "NXAK4.1B":[r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Controls/4.1B/2021_04_02_Transition_Imaging",
                r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Controls/4.1B/2021_04_05_Transition_Behaviour",
                r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Controls/4.1B/2021_04_08_Transition_Imaging",
                r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Controls/4.1B/2021_04_09_Transition_Behaviour",
                r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Controls/4.1B/2021_04_10_Transition_Imaging"],

    "NXAK7.1B":[r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Controls/7.1B/2021_03_22_Transition_Behaviour",
                r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Controls/7.1B/2021_03_23_Transition_Imaging",
                r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Controls/7.1B/2021_03_24_Transition_Behaviour",
                r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Controls/7.1B/2021_03_27_Transition_Imaging",
                r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Controls/7.1B/2021_03_30_Transition_Behaviour",
                r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Controls/7.1B/2021_03_31_Transition_Imaging",
                r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Controls/7.1B/2021_04_01_Transition_Behaviour",
                r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Controls/7.1B/2021_04_02_Transition_Imaging"],

    "NXAK14.1A":[r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Controls/14.1A/2021_06_12_Transition_Behaviour",
                r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Controls/14.1A/2021_06_13_Transition_Imaging",
                r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Controls/14.1A/2021_06_14_Transition_Behaviour",
                r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Controls/14.1A/2021_06_15_Transition_Imaging",
                r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Controls/14.1A/2021_06_16_Transition_Behaviour",
                r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Controls/14.1A/2021_06_17_Transition_Behaviour"],

    "NXAK22.1A":[r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Controls/22.1A/2021_10_26_Transition_Imaging",
                r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Controls/22.1A/2021_10_29_Transition_Imaging",
                r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Controls/22.1A/2021_11_02_Transition_Behaviour",
                r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Controls/22.1A/2021_11_03_Transition_Imaging",
                r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Controls/22.1A/2021_11_04_Transition_Behaviour",
                r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Controls/22.1A/2021_11_05_Transition_Imaging"]}


mutant_session_list = {

    "NXAK4.1A":[r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Mutants/4.1A/2021_04_08_Transition_Imaging",
                r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Mutants/4.1A/2021_04_10_Transition_Imaging",
                r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Mutants/4.1A/2021_04_11_Transition_Behaviour",
                r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Mutants/4.1A/2021_04_12_Transition_Imaging"],

    "NXAK10.1A":[r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Mutants/10.1A/2021_06_13_Transition_Behaviour",
                r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Mutants/10.1A/2021_06_14_Transition_Imaging",
                r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Mutants/10.1A/2021_06_16_Transition_Imaging",
                r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Mutants/10.1A/2021_06_17_Transition_Behaviour",
                r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Mutants/10.1A/2021_06_18_Transition_Imaging"],

    "NXAK20.1B":[r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Mutants/20.1B/2021_11_22_Transition_Imaging",
                r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Mutants/20.1B/2021_11_23_Transition_Behaviour",
                r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Mutants/20.1B/2021_11_24_Transition_Imaging",
                r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Mutants/20.1B/2021_11_26_Transition_Imaging"],

    "NXAK24.1C":[r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Mutants/24.1C/2021_11_05_Transition_Imaging",
                r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Mutants/24.1C/2021_11_08_Transition_Imaging",
                r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Mutants/24.1C/2021_11_10_Transition_Imaging"]
}





#    "NXAK16.1B":28,
#    "NRXN71.2A":21,


controls_days_to_learn = {
    "NXAK4.1B": 19,
    "NXAK7.1B": 24,
    "NXAK14.1A":11,
    "NXAK22.1A":16,
    "NRXN78.1A": 9,
    "NRXN78.1D": 13,
}

mutants_days_to_learn = {
    "NXAK4.1A":28,
    "NXAK10.1A": 15,
    "NXAK20.1B":23,
    "NXAK24.1C": 18,
    "NXAK16.1B":28,
    "NRXN71.2A":21,
}



control_mice_list = [
    "NXAK4.1B",
    "NXAK7.1B",
    "NXAK14.1A",
    "NXAK22.1A",

]

control_root_directories = {
                            "NXAK4.1B":r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Controls/4.1B",
                            "NXAK7.1B":r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Controls/7.1B",
                            "NXAK22.1A":r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Controls/22.1A",
                            "NXAK14.1A":r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Controls/14.1A",
                            "NRXN78.1A":r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Controls/78.1A",
                            "NRXN78.1D":r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Controls/78.1D"
}


mutant_mice_list = [
    "NXAK4.1A",
    "NXAK10.1A",
    "NXAK16.1B",
    "NXAK20.1B",
    "NXAK24.1C",
]



mutant_root_directories = {
"NRXN71.2A":r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Mutants/71.2A",
"NXAK4.1A":r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Mutants/4.1A",
"NXAK10.1A":r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Mutants/10.1A",
"NXAK20.1B":r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Mutants/20.1B",
"NXAK24.1C":r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Mutants/24.1C",
"NXAK16.1B":r"/media/matthew/Seagate Expansion Drive/1TB Contents/Behaviour_Analysis/Mutants/16.1B"
}


control_days_to_learn_list = []
control_average_irrel_performance = []

for mouse in control_mice_list:

    mouse_root_directory = control_root_directories[mouse]
    mouse_session_list = create_transition_session_list(mouse_root_directory)
    days_to_learn = controls_days_to_learn[mouse]

    transition_average = []
    for session in mouse_session_list:

       # Load dictonary
        performance_dictionary = np.load(os.path.join(session, "Behavioural_Measures", "Performance_Dictionary.npy"), allow_pickle=True)[()]
        transition_distribution = performance_dictionary["odour_to_visual_transition_distribution"]
        transition_distribution = clean_transition_distribution(transition_distribution)
        if len(transition_distribution) > 0:
            mean_transition = np.mean(transition_distribution)
            transition_average.append(mean_transition)

    transition_average = np.mean(transition_average)
    control_days_to_learn_list.append(days_to_learn)
    control_average_irrel_performance.append(transition_average)



mutant_days_to_learn_list = []
mutant_average_irrel_performance = []
for mouse in mutant_mice_list:

    mouse_root_directory = mutant_root_directories[mouse]
    mouse_session_list = create_transition_session_list(mouse_root_directory)
    days_to_learn = mutants_days_to_learn[mouse]

    transition_average = []
    for session in mouse_session_list:

        # Load dictonary
        performance_dictionary = np.load(os.path.join(session, "Behavioural_Measures", "Performance_Dictionary.npy"), allow_pickle=True)[()]
        transition_distribution = performance_dictionary["odour_to_visual_transition_distribution"]
        transition_distribution = clean_transition_distribution(transition_distribution)
        if len(transition_distribution) > 0:
            mean_transition = np.mean(transition_distribution)
            print("mean transition", mean_transition)
            transition_average.append(mean_transition)


    transition_average = np.mean(transition_average)
    mutant_days_to_learn_list.append(days_to_learn)
    mutant_average_irrel_performance.append(transition_average)




days_to_learn_list = control_days_to_learn_list + mutant_days_to_learn_list
average_irrel_performance = control_average_irrel_performance + mutant_average_irrel_performance

print("Average irrel performance", average_irrel_performance)
correlation = pearsonr(days_to_learn_list, average_irrel_performance)
print("Correlation ", correlation)
plt.scatter(control_days_to_learn_list, control_average_irrel_performance, c='b')
plt.scatter(mutant_days_to_learn_list, mutant_average_irrel_performance, c='g')

plt.xlabel("Days To Learn")
plt.ylabel("Mean Transition")
plt.show()
